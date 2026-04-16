# Night-Flow Leak Detection Algorithm

## Formulation
Between 01:00 and 04:00, campus baseflow should reach minimum quiescent flow $Q_{min}$:

$$Q_{actual} > Q_{quiescent} + k \cdot \sigma$$

If nocturnal flow exceeds threshold for $> 45$ consecutive minutes, automated alert is raised.
