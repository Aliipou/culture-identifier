"""Pydantic models for API request/response schemas."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class AnalyzeRequest(BaseModel):
    """Request model for text analysis."""
    text: str = Field(..., min_length=50, max_length=5000, description="User text for analysis")
    mode: str = Field(default="detailed", description="Analysis mode: 'detailed' or 'quick'")
    top_k: int = Field(default=3, ge=1, le=10, description="Number of top matches to return")

    @validator('text')
    def validate_text(cls, v):
        """Validate text input."""
        v = v.strip()
        if len(v) < 50:
            raise ValueError("Text must be at least 50 characters")
        return v

    @validator('mode')
    def validate_mode(cls, v):
        """Validate mode input."""
        if v not in ['detailed', 'quick']:
            raise ValueError("Mode must be 'detailed' or 'quick'")
        return v


class CulturalMatch(BaseModel):
    """Model for a single cultural figure match."""
    name: str = Field(..., description="Name of the cultural figure")
    score: float = Field(..., ge=0.0, le=1.0, description="Similarity score")
    reason: str = Field(..., description="Explanation for the match")
    category: str = Field(..., description="Category: philosopher, writer, or artist")
    period: str = Field(..., description="Time period")
    key_themes: List[str] = Field(default_factory=list, description="Key themes")
    recommendation: Dict[str, str] = Field(default_factory=dict, description="Book/work recommendation")


class Projection(BaseModel):
    """Model for 2D projection data."""
    x: float
    y: float
    label: str


class AnalyzeResponse(BaseModel):
    """Response model for text analysis."""
    matches: List[CulturalMatch] = Field(..., description="Top cultural figure matches")
    projection: List[Projection] = Field(default_factory=list, description="2D projection coordinates")
    user_embedding_summary: Dict[str, Any] = Field(default_factory=dict, description="Summary of user embedding")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    index_size: int
