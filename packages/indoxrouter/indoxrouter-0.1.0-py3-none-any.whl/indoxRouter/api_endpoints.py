"""
API endpoints for the IndoxRouter client package.
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from .utils.database import execute_query
from .utils.auth import get_current_user
from .models.database import User, RequestLog, Credit
from .utils.config import get_config
from .providers import get_provider

# Configure logging
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/api/v1", tags=["Client API"])


# Model definitions
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


# API endpoints
@router.post("/generate", response_model=GenerateResponse)
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


@router.get("/models", response_model=List[ModelInfo])
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


@router.get("/providers", response_model=List[ProviderInfo])
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


@router.get("/user", response_model=UserInfo)
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


@router.get("/user/balance", response_model=BalanceInfo)
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
