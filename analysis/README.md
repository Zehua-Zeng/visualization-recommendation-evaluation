# ./logs - Raw Experiment Results

## Names

- Of 72 participants for the user study, 40 were students and 32 were professional participants.
- We name experiment results with "_participant***conditions***task_\__type_.json".
- _Conditions_ are:
  - a: movie
  - b: birdstrikes
  - c: CompassQL
  - d: Dziban
  - e: BFS
  - f: DFS
- _Types_ are:
  - _intv_: interview Q&A
  - _answer_: participant input answer for the current task
  - _bookmarked_: the bookmarked charts for the current task
  - _logs_: interaction logs during the current task
  - _ptask_: participant's answers for the post-task questionnaire
- For example, "pro3_ace_p3_logs.json" stores a professional participant (pro3)'s interaction logs for task 3.

## ./logs/.+\_logs\.json - Interaction Logs

Each interaction is stored in a dictionary which consists of three key/value pairs:

- Interaction: The description of the interaction
- Value: The shortened Vega-Lite specification of the interacted chart. If no chart is interacted, for example, for "scroll down" interaction, no chart is involved, the value would be an empty string.
- Time: The 13-digit Unix timestamp recording when the interaction took place.

## ./logs/pilots/ - Pilots

- For pilot1 and pilot2, the interface design was different from the current one, the post-task questionnaires store in the "qX.json", "X" is the task no.
- pilot1 and pilot2 were tested with 2 different conditions for task 2 and task 3.
- pilot3-5 are similar as current user study, just the bookmark requirements for task 3 and task 4 were "at least 3 bookmarks", right now are "at least 5 bookmarks"
