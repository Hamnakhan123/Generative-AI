# 💻 Code · Track 3 · Innovate with Generative AI

> Prepared by **Hamna Zahid Khan**, Junior Lecturer

Every script below is complete and runnable on its own, and each one is used by a session page that shows the real output it produced. Files named `*_project_*.py` are the full solutions to each session's real-life mini project.

[⬅ Back to the track](../README.md)

## ⚙️ Setup

```bash
pip install matplotlib pandas   # only charts and Session 7 need these
cd code
python session-01_modality_map.py
```

Notebooks (`.ipynb`) contain every Python example of a session, already executed with saved output. Open them from the Colab badge at the top of each session page, or locally with `jupyter notebook`.

Run every command from inside this `code/` folder so relative data paths resolve. In Session 7 run `session-07_make_data.py` first.

## 📂 Files

### [Session 1 · Generative AI for Creators: Foundations and Toolkit](../session-01-generative-ai-for-creators.md)

| File | What it does | How to run |
|---|---|---|
| [`session-01-generative-ai-for-creators.ipynb`](session-01-generative-ai-for-creators.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-01-generative-ai-for-creators.ipynb` |
| [`session-01_modality_map.py`](session-01_modality_map.py) | Map a creative task to the right Gen AI modality. | `python session-01_modality_map.py` |
| [`session-01_tiny_generator.py`](session-01_tiny_generator.py) | A tiny "generative model" you can read in one minute. | `python session-01_tiny_generator.py` |
| [`session-01_project_toolkit_planner.py`](session-01_project_toolkit_planner.py) | Mini project (full solution) — Creator Toolkit Planner. | `python session-01_project_toolkit_planner.py` |
| [`session-01_time_saved.png`](session-01_time_saved.png) | Chart created by the mini project | created by `python session-01_project_toolkit_planner.py` |

### [Session 2 · Creating Textual Content with Generative AI](../session-02-creating-textual-content.md)

| File | What it does | How to run |
|---|---|---|
| [`session-02-creating-textual-content.ipynb`](session-02-creating-textual-content.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-02-creating-textual-content.ipynb` |
| [`session-02_prompt_builder.py`](session-02_prompt_builder.py) | A reusable prompt builder for written content. | `python session-02_prompt_builder.py` |
| [`session-02_readability.py`](session-02_readability.py) | Measure readability of an AI draft vs an edited draft. | `python session-02_readability.py` |
| [`session-02_platform_fit.py`](session-02_platform_fit.py) | Check social posts against platform rules before posting. | `python session-02_platform_fit.py` |
| [`session-02_project_blog_pipeline.py`](session-02_project_blog_pipeline.py) | Mini project (full solution) — A blog-writing pipeline. | `python session-02_project_blog_pipeline.py` |

### [Session 3 · Creating Visual Designs: Images, Posters and Presentations](../session-03-creating-visual-designs.md)

| File | What it does | How to run |
|---|---|---|
| [`session-03-creating-visual-designs.ipynb`](session-03-creating-visual-designs.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-03-creating-visual-designs.ipynb` |
| [`session-03_image_prompt_builder.py`](session-03_image_prompt_builder.py) | Build image prompts from parts, plus pixel sizes. | `python session-03_image_prompt_builder.py` |
| [`session-03_contrast_checker.py`](session-03_contrast_checker.py) | Is the text on your AI poster readable? (WCAG contrast) | `python session-03_contrast_checker.py` |
| [`session-03_slide_outline.py`](session-03_slide_outline.py) | From a topic to a presentation outline that a slide | `python session-03_slide_outline.py` |
| [`session-03_project_poster.py`](session-03_project_poster.py) | Mini project (full solution) — Generate an event poster in code. | `python session-03_project_poster.py` |
| [`session-03_poster.png`](session-03_poster.png) | Poster created by the mini project | created by `python session-03_project_poster.py` |

### [Session 4 · Creating Audio and Video with Generative AI](../session-04-creating-audio-and-video.md)

| File | What it does | How to run |
|---|---|---|
| [`session-04-creating-audio-and-video.ipynb`](session-04-creating-audio-and-video.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-04-creating-audio-and-video.ipynb` |
| [`session-04_script_timer.py`](session-04_script_timer.py) | How long will my narration be? | `python session-04_script_timer.py` |
| [`session-04_srt_maker.py`](session-04_srt_maker.py) | Generate a subtitle (.srt) file from a timed script. | `python session-04_srt_maker.py` |
| [`session-04_jingle.py`](session-04_jingle.py) | Make sound from numbers: a 2-second jingle. | `python session-04_jingle.py` |
| [`session-04_project_storyboard.py`](session-04_project_storyboard.py) | Mini project (full solution) — Storyboard to edit plan. | `python session-04_project_storyboard.py` |
| [`session-04_waveform.png`](session-04_waveform.png) | Waveform chart of the synthesised jingle | created by `python session-04_jingle.py` (which also writes `session-04_jingle.wav`, not committed) |
| [`session-04_promo.srt`](session-04_promo.srt) | Subtitle file produced by the SRT example | created by `python session-04_srt_maker.py` |
| [`session-04_edit_plan.json`](session-04_edit_plan.json) | Machine-readable edit plan from the storyboard project | created by `python session-04_project_storyboard.py` |

### [Session 5 · Storytelling with Generative AI](../session-05-storytelling-with-generative-ai.md)

| File | What it does | How to run |
|---|---|---|
| [`session-05-storytelling-with-generative-ai.ipynb`](session-05-storytelling-with-generative-ai.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-05-storytelling-with-generative-ai.ipynb` |
| [`session-05_story_arc.py`](session-05_story_arc.py) | Plan a story's structure before asking AI to write it. | `python session-05_story_arc.py` |
| [`session-05_character_sheet.py`](session-05_character_sheet.py) | A character bible that keeps AI stories consistent. | `python session-05_character_sheet.py` |
| [`session-05_branching_story.py`](session-05_branching_story.py) | Check an interactive (choose-your-own-path) story. | `python session-05_branching_story.py` |
| [`session-05_project_story_bible.py`](session-05_project_story_bible.py) | Mini project (full solution) — Story bible + continuity checker. | `python session-05_project_story_bible.py` |
| [`session-05_tension_curve.png`](session-05_tension_curve.png) | Planned tension curve chart | created by `python session-05_story_arc.py` |

### [Session 6 · Planning Complex Tasks: Events, Campaigns and Projects](../session-06-planning-complex-tasks.md)

| File | What it does | How to run |
|---|---|---|
| [`session-06-planning-complex-tasks.ipynb`](session-06-planning-complex-tasks.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-06-planning-complex-tasks.ipynb` |
| [`session-06_critical_path.py`](session-06_critical_path.py) | Critical path of an event plan (CPM). | `python session-06_critical_path.py` |
| [`session-06_event_checklist.py`](session-06_event_checklist.py) | Back-schedule an event checklist from its date. | `python session-06_event_checklist.py` |
| [`session-06_campaign_budget.py`](session-06_campaign_budget.py) | Split a campaign budget and forecast results. | `python session-06_campaign_budget.py` |
| [`session-06_project_campaign_planner.py`](session-06_project_campaign_planner.py) | Mini project (full solution) — Campaign planner with a Gantt chart. | `python session-06_project_campaign_planner.py` |
| [`session-06_gantt.png`](session-06_gantt.png) | Gantt chart of the campaign plan | created by `python session-06_project_campaign_planner.py` |

### [Session 7 · Analysing and Optimising Content Strategies](../session-07-analyzing-and-optimizing-content.md)

| File | What it does | How to run |
|---|---|---|
| [`session-07-analyzing-and-optimizing-content.ipynb`](session-07-analyzing-and-optimizing-content.ipynb) | Executed notebook with every Python example of the session | Colab badge on the session page, or `jupyter notebook session-07-analyzing-and-optimizing-content.ipynb` |
| [`session-07_make_data.py`](session-07_make_data.py) | create a SYNTHETIC posts dataset for the examples. | `python session-07_make_data.py` |
| [`session-07_metrics.py`](session-07_metrics.py) | Compute content KPIs from a dashboard export. | `python session-07_metrics.py` |
| [`session-07_best_time.py`](session-07_best_time.py) | When should we post? Engagement by hour and weekday. | `python session-07_best_time.py` |
| [`session-07_ab_test.py`](session-07_ab_test.py) | Did headline B really win? A two-proportion z-test. | `python session-07_ab_test.py` |
| [`session-07_project_content_audit.py`](session-07_project_content_audit.py) | Mini project (full solution) — A monthly content audit. | `python session-07_project_content_audit.py` |
| [`session-07_posts.csv`](session-07_posts.csv) | Synthetic 60-post analytics export used by all Session 7 scripts | created by `python session-07_make_data.py` |
| [`session-07_er_by_format.png`](session-07_er_by_format.png) | Engagement-rate-by-format chart from the audit | created by `python session-07_project_content_audit.py` |

---

<sub>Prepared by **Hamna Zahid Khan**, Junior Lecturer</sub>
