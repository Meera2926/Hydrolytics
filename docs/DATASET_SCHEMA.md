# Campus Water Consumption Telemetry - Dataset Schema

| Column Name | Data Type | Description | Unit |
| :--- | :--- | :--- | :--- |
| `Timestamp` | DateTime | Telemetry reading time | ISO 8601 |
| `Zone` | String | Campus sub-metering zone | Category |
| `FlowRate` | Float | Instantaneous pipeline flow | Liters/min |
| `TotalConsumption` | Float | Cumulative meter volume | Liters |
| `PressureBar` | Float | Mains supply pressure | Bar |
| `Occupancy` | Integer | Estimated building occupants | Count |
