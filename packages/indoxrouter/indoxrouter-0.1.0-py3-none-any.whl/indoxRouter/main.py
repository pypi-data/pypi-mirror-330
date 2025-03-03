"""
Main FastAPI application for IndoxRouter.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

# Import utility modules
from .utils.database import execute_query, close_all_connections
from .utils.auth import (
    verify_api_key,
    authenticate_user,
    generate_jwt_token,
    verify_jwt_token,
    AuthManager,
)
from .models.database import User, ApiKey, RequestLog, ProviderConfig, Credit
from .utils.config import get_config
from .providers import get_provider

# Import API endpoints router (will be created later)
# from .api_endpoints import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Load configuration
def load_config():
    """Load configuration from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in configuration file at {config_path}")
        return {}


config = load_config()

# Create FastAPI app
app = FastAPI(
    title="IndoxRouter API",
    description="A unified API for multiple LLM providers",
    version="0.1.0",
)

# Add CORS middleware
cors_origins = config.get("api", {}).get("cors_origins", ["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key security
api_key_header = APIKeyHeader(name="X-API-Key")

# Create the auth manager
auth_manager = AuthManager()


# Define request and response models
class CompletionRequest(BaseModel):
    provider: str = Field(..., description="The LLM provider to use")
    model: str = Field(..., description="The model to use")
    prompt: str = Field(..., description="The prompt to send to the model")
    max_tokens: Optional[int] = Field(
        None, description="Maximum number of tokens to generate"
    )
    temperature: Optional[float] = Field(0.7, description="Temperature for sampling")
    top_p: Optional[float] = Field(1.0, description="Top-p sampling parameter")
    stop: Optional[List[str]] = Field(
        None, description="Sequences where the API will stop generating"
    )
    stream: Optional[bool] = Field(False, description="Whether to stream the response")


class CompletionResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the completion")
    provider: str = Field(..., description="The provider used")
    model: str = Field(..., description="The model used")
    text: str = Field(..., description="The generated text")
    usage: Dict[str, int] = Field(..., description="Token usage information")
    created_at: datetime = Field(..., description="Timestamp of creation")


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class LoginResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiry in seconds")
    user_id: int = Field(..., description="User ID")
    is_admin: bool = Field(False, description="Whether the user is an admin")


class ApiKeyRequest(BaseModel):
    key_name: str = Field(..., description="Name for the API key")
    expires_days: Optional[int] = Field(
        None, description="Days until expiry (None for no expiry)"
    )


class ApiKeyResponse(BaseModel):
    key: str = Field(..., description="The generated API key")
    key_id: int = Field(..., description="ID of the API key")
    key_name: str = Field(..., description="Name of the API key")
    expires_at: Optional[datetime] = Field(None, description="Expiry date")


# Authentication dependency
async def get_current_user(authorization: str = None):
    """
    Get the current user from the API key.

    Args:
        authorization: Authorization header

    Returns:
        User data
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="API key is required")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    api_key = authorization.replace("Bearer ", "")

    user_data = auth_manager.verify_api_key(api_key)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user_data


# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to IndoxRouter", "version": "1.0.0"}


@app.post("/v1/completions", response_model=CompletionResponse)
async def create_completion(
    request: CompletionRequest,
    user_data: Dict[str, Any] = Depends(get_current_user),
    req: Request = None,
):
    """Create a completion using the specified provider."""
    try:
        # Get the provider
        provider_instance = get_provider(request.provider)
        if not provider_instance:
            raise HTTPException(
                status_code=400, detail=f"Provider '{request.provider}' not found"
            )

        # Generate the completion
        start_time = time.time()
        response = provider_instance.generate(
            model=request.model,
            prompt=request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            stop=request.stop,
        )
        process_time = time.time() - start_time

        # Log the request
        from indoxRouter.utils.database import get_session

        session = get_session()
        try:
            log = RequestLog(
                user_id=user_data["id"],
                api_key_id=user_data["api_key_id"],
                provider=request.provider,
                model=request.model,
                prompt=request.prompt,
                response=response,
                tokens_input=len(request.prompt.split()),
                tokens_output=len(response.split()),
                latency_ms=int(process_time * 1000),
                status_code=200,
                ip_address=req.client.host if req else None,
                user_agent=req.headers.get("User-Agent") if req else None,
            )
            session.add(log)
            session.commit()
        except Exception as e:
            logger.error(f"Error logging request: {e}")
            session.rollback()
        finally:
            session.close()

        # Return the response
        return {
            "id": f"cmpl-{int(time.time())}",
            "provider": request.provider,
            "model": request.model,
            "text": response,
            "usage": {
                "prompt_tokens": len(request.prompt.split()),
                "completion_tokens": len(response.split()),
                "total_tokens": len(request.prompt.split()) + len(response.split()),
            },
            "created_at": datetime.now(),
        }
    except Exception as e:
        logger.error(f"Error creating completion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating completion: {str(e)}",
        )


@app.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login endpoint to get JWT tokens."""
    user = authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, refresh_token, expires_in, _ = generate_jwt_token(
        user["id"], user["is_admin"]
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user_id": user["id"],
        "is_admin": user["is_admin"],
    }


@app.post("/auth/refresh", response_model=Dict[str, Any])
async def refresh_token(refresh_token: str):
    """Refresh an access token using a refresh token."""
    result = verify_jwt_token(refresh_token)
    if not result or result.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get new access token
    access_token, expires_in = result

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": expires_in,
    }


@app.post("/api-keys", response_model=ApiKeyResponse)
async def create_api_key(
    request: ApiKeyRequest, user_data: Dict[str, Any] = Depends(get_current_user)
):
    """Create a new API key for the current user."""
    try:
        api_key, key_id = auth_manager.generate_api_key(
            user_id=user_data["id"],
            key_name=request.key_name,
            expires_days=request.expires_days,
        )

        # Get the key record
        key_record = ApiKey.get_by_id(key_id)

        return {
            "key": api_key,
            "key_id": key_id,
            "key_name": key_record["key_name"],
            "expires_at": key_record["expires_at"],
        }
    except Exception as e:
        logger.error(f"Error creating API key: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating API key: {str(e)}",
        )


@app.get("/api-keys", response_model=List[Dict[str, Any]])
async def list_api_keys(user_data: Dict[str, Any] = Depends(get_current_user)):
    """List all API keys for the current user."""
    try:
        keys = ApiKey.list_by_user(user_data["id"])
        return keys
    except Exception as e:
        logger.error(f"Error listing API keys: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing API keys: {str(e)}",
        )


@app.delete("/api-keys/{key_id}", response_model=Dict[str, bool])
async def delete_api_key(
    key_id: int, user_data: Dict[str, Any] = Depends(get_current_user)
):
    """Delete an API key."""
    try:
        # Check if the key belongs to the user
        key = ApiKey.get_by_id(key_id)
        if not key or key["user_id"] != user_data["id"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="API key not found"
            )

        # Delete the key
        success = ApiKey.delete_key(key_id)
        return {"success": success}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting API key: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting API key: {str(e)}",
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Starting IndoxRouter application")

    # TODO: Initialize any resources needed at startup


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Shutting down IndoxRouter application")

    # Close database connections
    close_all_connections()


# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"},
    )


# New API endpoints for the client package


class GenerateRequest(BaseModel):
    """Request model for text generation."""

    prompt: str = Field(..., description="The prompt to send to the model")
    model: Optional[str] = Field(None, description="The model to use")
    provider: Optional[str] = Field(None, description="The provider to use")
    temperature: Optional[float] = Field(0.7, description="Temperature for sampling")
    max_tokens: Optional[int] = Field(
        1000, description="Maximum number of tokens to generate"
    )
    top_p: Optional[float] = Field(1.0, description="Top-p sampling parameter")
    stop: Optional[List[str]] = Field(
        None, description="Sequences where the API will stop generating"
    )
    stream: Optional[bool] = Field(False, description="Whether to stream the response")


class GenerateResponse(BaseModel):
    """Response model for text generation."""

    id: str = Field(..., description="Unique identifier for the completion")
    text: str = Field(..., description="The generated text")
    provider: str = Field(..., description="The provider used")
    model: str = Field(..., description="The model used")
    usage: Dict[str, int] = Field(..., description="Token usage information")
    created_at: datetime = Field(..., description="Timestamp of creation")


class ModelInfo(BaseModel):
    """Model for LLM model information."""

    id: str = Field(..., description="Model identifier")
    name: str = Field(..., description="Model name")
    provider: str = Field(..., description="Provider name")
    description: Optional[str] = Field(None, description="Model description")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens supported")
    pricing: Optional[Dict[str, float]] = Field(None, description="Pricing information")


class ProviderInfo(BaseModel):
    """Model for LLM provider information."""

    id: str = Field(..., description="Provider identifier")
    name: str = Field(..., description="Provider name")
    description: Optional[str] = Field(None, description="Provider description")
    website: Optional[str] = Field(None, description="Provider website")
    models: List[str] = Field(..., description="Available models")


class UserInfo(BaseModel):
    """Model for user information."""

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    first_name: Optional[str] = Field(None, description="User first name")
    last_name: Optional[str] = Field(None, description="User last name")
    is_admin: bool = Field(False, description="Whether the user is an admin")
    created_at: datetime = Field(..., description="Account creation timestamp")


class BalanceInfo(BaseModel):
    """Model for user balance information."""

    credits: float = Field(..., description="Available credits")
    usage: Dict[str, float] = Field(..., description="Usage statistics")
    last_updated: datetime = Field(..., description="Last updated timestamp")


@app.post("/api/v1/generate", response_model=GenerateResponse)
async def generate(
    request: GenerateRequest,
    user_data: Dict[str, Any] = Depends(get_current_user),
    req: Request = None,
):
    """Generate text using the specified model and provider."""
    try:
        # Set default model and provider if not specified
        provider_name = request.provider or get_config().get(
            "default_provider", "openai"
        )
        model_name = request.model or get_config().get("default_model", "gpt-4o-mini")

        # Get the provider
        provider = get_provider(provider_name)
        if not provider:
            raise HTTPException(
                status_code=400, detail=f"Provider '{provider_name}' not found"
            )

        # Generate the completion
        completion = await provider.generate(
            model=model_name,
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            stop=request.stop,
            stream=request.stream,
        )

        # Log the request
        log_entry = RequestLog(
            user_id=user_data["user_id"],
            provider=provider_name,
            model=model_name,
            prompt_tokens=completion.get("usage", {}).get("prompt_tokens", 0),
            completion_tokens=completion.get("usage", {}).get("completion_tokens", 0),
            total_tokens=completion.get("usage", {}).get("total_tokens", 0),
            created_at=datetime.utcnow(),
        )
        execute_query(lambda session: session.add(log_entry))

        # Return the response
        return {
            "id": completion.get("id", ""),
            "text": completion.get("text", ""),
            "provider": provider_name,
            "model": model_name,
            "usage": completion.get("usage", {}),
            "created_at": datetime.utcnow(),
        }
    except Exception as e:
        logger.error(f"Error generating completion: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/models", response_model=List[ModelInfo])
async def list_models(
    provider: Optional[str] = None,
    user_data: Dict[str, Any] = Depends(get_current_user),
):
    """List available models, optionally filtered by provider."""
    try:
        # Get configuration
        config = get_config()
        models = []

        # If provider is specified, only get models for that provider
        if provider:
            provider_obj = get_provider(provider)
            if not provider_obj:
                raise HTTPException(
                    status_code=400, detail=f"Provider '{provider}' not found"
                )
            provider_models = provider_obj.list_models()
            for model in provider_models:
                models.append(
                    {
                        "id": model.get("id", ""),
                        "name": model.get("name", ""),
                        "provider": provider,
                        "description": model.get("description", ""),
                        "max_tokens": model.get("max_tokens", 0),
                        "pricing": model.get("pricing", {}),
                    }
                )
        else:
            # Get models for all providers
            for provider_name in config.get("providers", {}).keys():
                try:
                    provider_obj = get_provider(provider_name)
                    if provider_obj:
                        provider_models = provider_obj.list_models()
                        for model in provider_models:
                            models.append(
                                {
                                    "id": model.get("id", ""),
                                    "name": model.get("name", ""),
                                    "provider": provider_name,
                                    "description": model.get("description", ""),
                                    "max_tokens": model.get("max_tokens", 0),
                                    "pricing": model.get("pricing", {}),
                                }
                            )
                except Exception as e:
                    logger.error(
                        f"Error getting models for provider {provider_name}: {str(e)}"
                    )

        return models
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/providers", response_model=List[ProviderInfo])
async def list_providers(
    user_data: Dict[str, Any] = Depends(get_current_user),
):
    """List available providers."""
    try:
        # Get configuration
        config = get_config()
        providers = []

        # Get all providers
        for provider_name, provider_config in config.get("providers", {}).items():
            try:
                provider_obj = get_provider(provider_name)
                if provider_obj:
                    provider_models = provider_obj.list_models()
                    providers.append(
                        {
                            "id": provider_name,
                            "name": provider_config.get("name", provider_name),
                            "description": provider_config.get("description", ""),
                            "website": provider_config.get("website", ""),
                            "models": [
                                model.get("id", "") for model in provider_models
                            ],
                        }
                    )
            except Exception as e:
                logger.error(f"Error getting provider {provider_name}: {str(e)}")

        return providers
    except Exception as e:
        logger.error(f"Error listing providers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/user", response_model=UserInfo)
async def get_user(
    user_data: Dict[str, Any] = Depends(get_current_user),
):
    """Get information about the authenticated user."""
    try:
        # Get user from database
        user = None

        def get_user_from_db(session):
            nonlocal user
            user = session.query(User).filter(User.id == user_data["user_id"]).first()
            return user

        execute_query(get_user_from_db)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
            "created_at": user.created_at,
        }
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/user/balance", response_model=BalanceInfo)
async def get_balance(
    user_data: Dict[str, Any] = Depends(get_current_user),
):
    """Get the user's current balance."""
    try:
        # Get user's credit from database
        credit = None
        usage_data = {}

        def get_credit_from_db(session):
            nonlocal credit
            credit = (
                session.query(Credit)
                .filter(Credit.user_id == user_data["user_id"])
                .first()
            )
            return credit

        def get_usage_from_db(session):
            nonlocal usage_data
            # Get total usage by provider
            usage_by_provider = {}
            logs = (
                session.query(RequestLog)
                .filter(RequestLog.user_id == user_data["user_id"])
                .all()
            )
            for log in logs:
                provider = log.provider
                if provider not in usage_by_provider:
                    usage_by_provider[provider] = 0
                usage_by_provider[provider] += log.total_tokens

            usage_data = usage_by_provider
            return usage_by_provider

        execute_query(get_credit_from_db)
        execute_query(get_usage_from_db)

        if not credit:
            # Create a new credit entry with default values
            credit = Credit(
                user_id=user_data["user_id"],
                amount=0.0,
                last_updated=datetime.utcnow(),
            )
            execute_query(lambda session: session.add(credit))

        return {
            "credits": credit.amount,
            "usage": usage_data,
            "last_updated": credit.last_updated,
        }
    except Exception as e:
        logger.error(f"Error getting balance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# If this file is run directly, start the application with Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
