from typing import Literal

from pydantic import BaseModel, Field


class SkillGroup(BaseModel):
    required: list[str] = Field(default_factory=list)
    preferred: list[str] = Field(default_factory=list)


class JDSkills(BaseModel):
    technical_skills: SkillGroup
    tools_and_frameworks: SkillGroup
    soft_skills: SkillGroup


class ResumeSkills(BaseModel):
    technical_skills: list[str] = Field(default_factory=list)
    tools_and_frameworks: list[str] = Field(default_factory=list)
    soft_skills: list[str] = Field(default_factory=list)


class CategoryGap(BaseModel):
    matched: list[str] = Field(default_factory=list)
    missing_required: list[str] = Field(default_factory=list)
    missing_preferred: list[str] = Field(default_factory=list)


class GapAnalysis(BaseModel):
    technical_skills: CategoryGap
    tools_and_frameworks: CategoryGap
    soft_skills: CategoryGap


class RoadmapItem(BaseModel):
    skill: str
    category: Literal["technical_skills", "tools_and_frameworks", "soft_skills"]
    priority: Literal["required", "preferred"]
    project_title: str
    project_description: str
    proof_of_skill: str
    estimated_time: str
    difficulty: Literal["beginner", "intermediate", "advanced"]


class Roadmap(BaseModel):
    projects: list[RoadmapItem] = Field(default_factory=list)


class AnalyzeRequest(BaseModel):
    job_description: str = Field(min_length=1)
    resume_text: str = Field(min_length=1)


class AnalyzeResponse(BaseModel):
    gap_analysis: GapAnalysis
    roadmap: Roadmap
