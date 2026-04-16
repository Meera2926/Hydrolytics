# Hydrolytics REST API Documentation

## 1. Predict Demand
- **POST** `/predict`
- **Body**:
```json
{
  "zone": "Hostel Block",
  "hour": 14,
  "occupancy": 350
}
```
- **Response** (200 OK):
```json
{
  "predicted_demand_liters": 257.5,
  "status": "NORMAL"
}
```
