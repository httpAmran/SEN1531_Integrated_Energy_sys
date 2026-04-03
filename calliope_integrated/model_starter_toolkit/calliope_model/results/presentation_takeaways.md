# Wind Surplus Scenario Takeaways (Fresh Model Run)

Scenarios solved: `default`, `surplus_to_battery`, `surplus_to_hydrogen`, `surplus_to_big_user`, `surplus_to_big_user_two_nodes`.

## Executive takeaways

1. **Baseline curtailment opportunity is very large**: 123.3 TWh curtailed (31.7% of available wind).
2. **Best curtailment reduction** is `surplus_to_hydrogen`: -32.9 TWh vs default (26.7%).
3. **Best revenue uplift** is `surplus_to_big_user_two_nodes`: +1018.1 M EUR/year (18.5%).
4. **Lowest LCOE** is `surplus_to_big_user_two_nodes`: 0.0081 kEUR/MWh (about 24.2% below default).
5. **Battery pathway** cuts curtailment strongly (29.3 TWh) with ~89.9% round-trip efficiency, but requires highest capex proxy (+17400.0 M EUR).
6. **Hydrogen pathway** absorbs 32.9 TWh via electrolyser input and gives the largest drop in negative-price hours (67.0% -> 58.1%).
7. **Big-user demand sink** in two-node form serves 22.5 TWh/year (~2564 MW average), outperforming one-node big-user (14.3 TWh/year).
8. **Security of supply stays intact** in all runs: load shedding is negligible relative to annual demand.

## Scenario snapshot

| Scenario | Curtailment (TWh) | Curtailment rate (%) | LCOE (kEUR/MWh) | Revenue (M EUR) | Capex proxy (M EUR) | Negative-price hours (%) |
|---|---:|---:|---:|---:|---:|---:|
| default | 123.3 | 31.7 | 0.0107 | 5500.4 | 123838.2 | 67.0 |
| surplus_to_battery | 94.0 | 24.2 | 0.0085 | 5632.6 | 141238.2 | 68.1 |
| surplus_to_hydrogen | 90.4 | 23.2 | 0.0106 | 5580.5 | 125518.2 | 58.1 |
| surplus_to_big_user | 109.0 | 28.0 | 0.0104 | 5633.9 | 123838.2 | 63.4 |
| surplus_to_big_user_two_nodes | 100.4 | 25.8 | 0.0081 | 6518.5 | 123838.2 | 61.1 |

## Interpretation for project narrative

- The system has a structural wind-surplus issue in baseline operation, so surplus-routing pathways are justified.
- Hydrogen is strongest for physically reducing curtailed wind and lowering negative-price exposure.
- Two-node big-user pathway is strongest on economic KPIs under current tariff and line-cost assumptions.
- Battery is effective technically but has the highest incremental capex burden in this setup.

## Modeling caveat to mention in presentation

- Big-user and hydrogen outcomes are sensitive to assumed value proxies (`cost_flow_in`) and line capex settings; these are policy/commercial assumptions, not measured market contracts.