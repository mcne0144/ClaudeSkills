# Greenway: service win-back: decisioning report

Generated 2026-10-24T12:00:00+00:00. Mode: lifecycle.

## Experiment groups

| Group | Users |
|---|---|
| treatment | 2422 |
| holdout | 578 |
| customer_managed | 0 |

## Lift vs holdout (incrementality)

### service_booked (best, 7-day window)

| Group | Matured users | Converters | Rate | 95% CI |
|---|---|---|---|---|
| treatment | 2422 | 830 | 34.27% | 32.41% to 36.18% |
| holdout | 578 | 116 | 20.07% | 17.01% to 23.53% |

Absolute lift 14.20% (95% CI 10.27% to 17.81%). Relative lift 70.8%. p = 0.000. significant at 95%.

### unsubscribed (worst, 7-day window)

| Group | Matured users | Converters | Rate | 95% CI |
|---|---|---|---|---|
| treatment | 2422 | 24 | 0.99% | 0.67% to 1.47% |
| holdout | 578 | 0 | 0.00% | 0.00% to 0.66% |

Difference (treatment minus holdout, lower is better) 0.99% (95% CI 0.26% to 1.47%). p = 0.016. significant at 95%.

## Sends

| Action | Count |
|---|---|
| send | 5499 |
| suppressed | 948 |

## Creative performance

| Message | Channel | Sends | Matured | Conv | Rate | 95% CI | Posterior | Bad outcomes |
|---|---|---|---|---|---|---|---|---|
| Service SMS, $25 off | sms | 1397 | 1397 | 190 | 13.60% | 11.90% to 15.50% | 14.26% | 7 |
| Service reminder, $25 off | email | 2051 | 2051 | 253 | 12.34% | 10.98% to 13.83% | 12.74% | 10 |
| Service reminder, safety check | email | 2051 | 2051 | 191 | 9.31% | 8.13% to 10.65% | 9.45% | 7 |

## Variant performance

| Message | Type | Variant | Sends | Conv | Posterior |
|---|---|---|---|---|---|
| email_offer | subject | s2: Your {vehicle} is due. Save $25 | 1401 | 189 | 14.00% |
| email_offer | subject | s1: $25 off your next oil change | 650 | 64 | 10.14% |
| email_safety | subject | s1: A quick check before winter | 1162 | 114 | 10.08% |
| email_safety | subject | s2: Is your {vehicle} ready for the cold? | 889 | 77 | 8.72% |
| sms_offer | body | b1: Greenway: $25 off your oil change this month. Book | 1397 | 190 | 14.26% |

## Timing (conversion rate by send day and time of day, user local)

| Day | morning | afternoon | evening | night |
|---|---|---|---|---|
| mon | 11.95% (n=293) | 13.40% (n=321) | 15.64% (n=697) |  |
| tue | 15.15% (n=66) | 12.66% (n=79) | 15.42% (n=227) |  |
| wed | 0.00% (n=5) | 16.67% (n=12) | 22.86% (n=35) |  |
| thu | 0.00% (n=3) | 100.00% (n=1) | 0.00% (n=5) |  |
| fri |  |  |  |  |
| sat | 8.61% (n=685) | 7.75% (n=671) | 11.02% (n=590) |  |
| sun | 9.82% (n=550) | 9.65% (n=373) | 12.98% (n=886) |  |

## Personalization matrix (conversion rate by user feature and creative tag)

### segment x offer_type

| segment | discount | none |
|---|---|---|
| a | 12.13% (n=1138) | 9.78% (n=675) |
| b | 12.23% (n=1128) | 10.57% (n=662) |
| c | 14.13% (n=1182) | 7.70% (n=714) |

### segment x tone

| segment | caring | urgent |
|---|---|---|
| a | 9.78% (n=675) | 12.13% (n=1138) |
| b | 10.57% (n=662) | 12.23% (n=1128) |
| c | 7.70% (n=714) | 14.13% (n=1182) |

### vehicle_age x offer_type

| vehicle_age | discount | none |
|---|---|---|
| high | 14.80% (n=1432) | 8.74% (n=721) |
| low | 12.86% (n=653) | 10.57% (n=653) |
| mid | 10.79% (n=1363) | 8.71% (n=677) |

### vehicle_age x tone

| vehicle_age | caring | urgent |
|---|---|---|
| high | 8.74% (n=721) | 14.80% (n=1432) |
| low | 10.57% (n=653) | 12.86% (n=653) |
| mid | 8.71% (n=677) | 10.79% (n=1363) |

## Recommendations

- Expand the winner: 'Service SMS, $25 off' leads at 13.60% on 1397 matured sends. Add variants in the same tone or offer type.
- Retire or rework 'Service reminder, safety check': its upper bound 10.65% sits below the leader's lower bound 11.90%.
- Coverage gaps: only one message carries each of tone=caring, offer_type=none. The model cannot separate the tag from the message until a second one exists.

## How to read this

Lift compares converters per matured user in treatment against holdout; it is incrementality, not last-touch attribution, so it will not match an ESP or ad platform dashboard. Posterior means are the model's current belief after pooling each context with the global estimate; they move before raw rates do. Confidence intervals are Wilson intervals; the lift interval is Newcombe's method.
