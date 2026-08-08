# Attempt 4 verdict sheet (demo-walk-protocol.md template, filled)

Filled by the recorder from James's rulings in-session 2026-08-08;
sub-verdicts and overall verdict are his words, quoted or tightly
paraphrased. Snaps: this folder (48 files, named by step).

```
WALK ------------------------------------------------------------
Date (UTC):            2026-08-08
Db file:               data/demo-walk-2026-08-08.db  (fresh: Y)
Marks M0..M6:          M0 05:44:02  M1 05:44:28  M2 05:53:52
                       M3 05:55:05  M4 05:59:23  M5 06:04:46
                       M6 06:07:47
                       (derived from snapshot file mtimes, local
                       clock; marks were not called in chat)
Elapsed M1->M6:        23:19  (soft budget 20:00; over by 3:19)
Dev-tools touched mid-walk (voids): N

FRICTION LOG (demo-readiness data)
 # | screen/step  | what happened                       | severity
---+--------------+-------------------------------------+---------
 1 | 29 (balance  | ledger links under the dollar tiles | unrated
   | tiles)       | are small underlined text; "always  |
   |              | miss them" (snap filename note)     |
 2 | whole walk   | no overall status surface: no       | verdict
   |              | project / client / matter / billing | driver
   |              | summary layer; "I don't feel like I |
   |              | have an overall status"             |
 3 | whole walk   | flow not visible in the UI: hidden  | verdict
   |              | state must be brought forward so    | driver
   |              | the user can follow the order (add  |
   |              | client -> matter -> bill -> which   |
   |              | type / which account -> collect vs  |
   |              | disburse); "sometimes I'm clicking  |
   |              | around"; "The UI does not bring out |
   |              | the structure of the actual code in |
   |              | a way that the user can logically   |
   |              | follow and reinforce a narrative"   |
 4 | whole walk   | general finish: "it's not           | unrated
   |              | beautiful"                          |
 5 | timing       | 23:19 elapsed vs 20:00 soft budget  | auto
   |              | (protocol: friction entry, never a  |
   |              | fail by itself)                     |

CLOSE-OUT
check_demo_walk.py exit 0:        Y  (12 PASS lines, fiduciary
                                     "8 pass, 0 red, 0 stub;
                                     verdict: GREEN" on the
                                     walked db; quoted in
                                     worklog s10)
PDF + ledger + recon eyeball:     Y  (walked steps 29-32; snaps
                                     29A/29B PDF, 29 tiles show
                                     800.00, 32 recon HOLDS both
                                     accounts)

SUB-VERDICTS (James, each up/down; ALL required for PASS)
(a) FIDUCIARY STORY LANDS:   PASS  ("I think it's just the
                                    product around it" -- the
                                    ledger / correction trail /
                                    recon trio made the case;
                                    recon traversed "easily")
(b) NOTHING EMBARRASSING:    FAIL  ("it's not beautiful";
                                    hesitant to show a demo)
(c) BOOKABLE:                FAIL  ("I'd be hesitant to show a
                                    demo")

VERDICT: FAIL (axes b + c: no overall status surface, flow
narrative not visible in the UI, finish below his standard.
NOT the attempt-3 axes -- reconciliation correctness and the
s7-s9 polish held.)
```
