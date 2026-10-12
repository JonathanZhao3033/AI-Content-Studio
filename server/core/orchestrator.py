"""
server/core/orchestrator.py

Unified Autonomous Content Creation Orchestrator that coordinates:
Strategy -> Trend Discovery -> Deep Research -> Storyboard & Scriptwriting ->
Technical & Creative QA -> Editing Timeline -> Export -> Learning.
"""

import os
import json
import logging
from typing import Dict, Any, Optional

from server.core.agent_system import (
    StrategyAgent, TrendDiscoveryAgent, ResearchAgent, 
    CreativeDirectorAgent, QualityAssuranceAgent, LearningAgent,
    VideoScriptPlan
)
from server.core.queue import update_job, add_log, save_stage_checkpoint
from config import load_config

class AutonomousStudioOrchestrator:
    def __init__(self, job_id: Optional[str] = None):
        self.job_id = job_id
        self.strategy_agent = StrategyAgent()
        self.trend_agent = TrendDiscoveryAgent()
        self.research_agent = ResearchAgent()
        self.director_agent = CreativeDirectorAgent()
        self.qa_agent = QualityAssuranceAgent()
        self.learning_agent = LearningAgent()

    def _log(self, msg: str):
        logging.info(f"[Orchestrator:{self.job_id}] {msg}")
        if self.job_id:
            add_log(self.job_id, msg)

    def _update_progress(self, step: str, progress: float):
        if self.job_id:
            update_job(self.job_id, step=step, progress=progress)

    def produce_content_pipeline(
        self, 
        topic: str, 
        duration_sec: int = 45, 
        style: str = "Cinematic Documentary", 
        region: str = "Global",
        auto_approve: bool = False
    ) -> Dict[str, Any]:
        """
        Executes end-to-end intelligent creative pipeline with checkpoints and validation.
        """
        self._log(f"Starting Autonomous Creative Production for topic: '{topic}'")
        self._update_progress("Synthesizing Strategy & Preferences", 0.05)

        # 1. Learning Check: Inject saved user preferences
        preferred_style = self.learning_agent.get_preference("user_preference", "default_style", style)
        self._log(f"Loaded active style profile: '{preferred_style}'")

        # 2. Research Phase
        self._update_progress("Deep Research & Fact Verification", 0.20)
        research = self.research_agent.research_topic(topic)
        self._log(f"Research complete: {len(research.key_insights)} insights, {len(research.facts_ledger)} verified facts.")
        if self.job_id:
            save_stage_checkpoint(self.job_id, "research", research.model_dump())

        # 3. Creative Storyboard & Scriptwriting
        self._update_progress("Directing Scenes & Writing Script", 0.45)
        script_plan = self.director_agent.create_storyboard_plan(
            topic=topic,
            research=research,
            target_duration_sec=duration_sec,
            style=preferred_style
        )
        self._log(f"Script planned: '{script_plan.title}' with {len(script_plan.scenes)} scenes.")

        # 4. Quality Assurance Review & Autonomous Self-Healing Retry Loop
        self._update_progress("Quality Assurance Inspection", 0.65)
        qa_result = self.qa_agent.review_plan(script_plan, research)
        self._log(f"Initial QA Score: {qa_result.score}/100. Passed: {qa_result.passed}")

        # Self-healing loop: if QA score < 80, automatically critique and rewrite
        max_retries = 2
        retry_count = 0
        while (not qa_result.passed or qa_result.score < 80) and retry_count < max_retries:
            retry_count += 1
            critique_feedback = (
                f"Issues to fix:\n"
                f"- Defects: {', '.join(qa_result.technical_defects) if qa_result.technical_defects else 'None'}\n"
                f"- Improvements needed: {', '.join(qa_result.creative_improvements)}\n"
                f"- Recommendations: {', '.join(qa_result.recommended_repairs)}"
            )
            self._log(f"QA threshold not met ({qa_result.score}/100). Triggering autonomous revision pass {retry_count}/{max_retries}...")
            self._update_progress(f"Autonomous Script Revision (Pass {retry_count})", 0.50 + (retry_count * 0.08))
            
            # Preserve any scenes marked locked
            locked = [s for s in script_plan.scenes if s.locked]
            script_plan = self.director_agent.create_storyboard_plan(
                topic=topic,
                research=research,
                target_duration_sec=duration_sec,
                style=preferred_style,
                feedback=critique_feedback,
                locked_scenes=locked
            )
            qa_result = self.qa_agent.review_plan(script_plan, research)
            self._log(f"Revision pass {retry_count} QA Score: {qa_result.score}/100. Passed: {qa_result.passed}")

        if self.job_id:
            save_stage_checkpoint(self.job_id, "storyboard", script_plan.model_dump())
            save_stage_checkpoint(self.job_id, "qa_review", qa_result.model_dump())

        # 5. Output Packaging
        output_data = {
            "topic": topic,
            "title": script_plan.title,
            "hook": script_plan.hook,
            "duration": script_plan.target_duration_sec,
            "style": preferred_style,
            "scenes": [s.model_dump() for s in script_plan.scenes],
            "research_summary": research.summary,
            "qa_score": qa_result.score,
            "qa_passed": qa_result.passed,
            "status": "ready_for_render" if auto_approve else "awaiting_approval"
        }

        if auto_approve:
            self._update_progress("Production Approved & Ready", 1.0)
            if self.job_id:
                update_job(self.job_id, status="completed", progress=1.0, result=json.dumps(output_data))
        else:
            self._update_progress("Awaiting User Approval", 0.75)
            if self.job_id:
                update_job(self.job_id, status="awaiting_approval", progress=0.75, result=json.dumps(output_data))

        # Store creative decision in memory
        self.learning_agent.record_preference("creative_memory", f"topic_{topic[:30]}", {
            "title": script_plan.title,
            "hook": script_plan.hook,
            "score": qa_result.score
        })

        self._log("Autonomous Orchestrator completed planning stage successfully.")
        return output_data

    @classmethod
    def regenerate_single_scene(cls, job_id: str, scene_number: int, instruction: str) -> Dict[str, Any]:
        """Regenerates a single scene in the storyboard and persists the updated plan."""
        from server.core.queue import get_stage_checkpoint, save_stage_checkpoint, get_job, update_job, manager
        from server.core.agent_system import ScriptScene, CreativeDirectorAgent

        storyboard_data = get_stage_checkpoint(job_id, "storyboard")
        if not storyboard_data:
            job = get_job(job_id)
            if job and job.get("result"):
                try:
                    res = json.loads(job["result"])
                    storyboard_data = res
                except Exception:
                    pass
        if not storyboard_data or "scenes" not in storyboard_data:
            raise ValueError(f"No storyboard plan found for job {job_id}")

        director = CreativeDirectorAgent()
        scenes = [ScriptScene(**s) for s in storyboard_data["scenes"]]
        target_scene_idx = next((i for i, s in enumerate(scenes) if s.scene_number == scene_number), None)
        if target_scene_idx is None:
            raise ValueError(f"Scene number {scene_number} not found in storyboard")

        # Regenerate target scene
        updated_scene = director.revise_scene(scenes[target_scene_idx], instruction)
        scenes[target_scene_idx] = updated_scene

        storyboard_data["scenes"] = [s.model_dump() for s in scenes]
        save_stage_checkpoint(job_id, "storyboard", storyboard_data)
        update_job(job_id, result=json.dumps(storyboard_data))
        manager.broadcast(job_id, {"type": "storyboard_updated", "data": storyboard_data})
        return storyboard_data

    @classmethod
    def update_storyboard_scenes(cls, job_id: str, updated_scenes: list) -> Dict[str, Any]:
        """Updates storyboard scene modifications (locks, edits) and persists them."""
        from server.core.queue import get_stage_checkpoint, save_stage_checkpoint, get_job, update_job, manager

        storyboard_data = get_stage_checkpoint(job_id, "storyboard")
        if not storyboard_data:
            job = get_job(job_id)
            if job and job.get("result"):
                try:
                    storyboard_data = json.loads(job["result"])
                except Exception:
                    pass
        if not storyboard_data:
            storyboard_data = {"scenes": []}

        storyboard_data["scenes"] = updated_scenes
        save_stage_checkpoint(job_id, "storyboard", storyboard_data)
        update_job(job_id, result=json.dumps(storyboard_data))
        manager.broadcast(job_id, {"type": "storyboard_updated", "data": storyboard_data})
        return storyboard_data
