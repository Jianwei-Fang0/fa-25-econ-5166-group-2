# Data Directory Structure

## Overview
This directory contains YouBike data processing pipeline for NTU area analysis.

## Directory Structure

### 📁 `/raw/` - Raw Data Files
| File Name | Description | Size | Period | Content |
|-----------|-------------|------|--------|---------|
| `202403_YouBike.csv` | Raw YouBike data | ~200MB+ | March 2024 | Original YouBike transaction records |
| `202404_YouBike.csv` | Raw YouBike data | ~200MB+ | April 2024 | Original YouBike transaction records |
| `202405_YouBike.csv` | Raw YouBike data | ~200MB+ | May 2024 | Original YouBike transaction records |
| `202406_YouBike.csv` | Raw YouBike data | ~200MB+ | June 2024 | Original YouBike transaction records |
| `202409_YouBike.csv` | Raw YouBike data | ~200MB+ | September 2024 | Original YouBike transaction records |
| `202410_YouBike.csv` | Raw YouBike data | ~200MB+ | October 2024 | Original YouBike transaction records |
| `202411_YouBike.csv` | Raw YouBike data | ~200MB+ | November 2024 | Original YouBike transaction records |
| `202412_YouBike.csv` | Raw YouBike data | ~200MB+ | December 2024 | Original YouBike transaction records |
| `202501_YouBike.csv` | Raw YouBike data | ~200MB+ | January 2025 | Original YouBike transaction records |

**Raw Data Schema:**
- `borrow_datetime`: Borrow time
- `borrow_site`: Borrow station name
- `return_datetime`: Return time  
- `return_site`: Return station name
- `borrowing_time`: Duration
- `bike_type`: Bike type (一般車/電輔車)
- `date`: Date

**Raw Data Schema Example:**
| borrow_datetime | borrow_site | return_datetime | return_site | borrowing_time | bike_type | date |
|-----------------|-------------|-----------------|-------------|----------------|-----------|------|
| 2025-01-13 15:00:00 | 捷運古亭站(8號出口) | 2025-01-13 21:00:00 | 新生南路三段52號前 | 05:34:25 | 電輔車 | 2025-01-13 |

### 📁 `/processed/` - Processed Data Files

#### 🚴‍♂️ NTU YouBike Data (`/ntu_youbike_data/`)
| File Name | Description | Records | Period | Content |
|-----------|-------------|---------|--------|---------|
| `ntu_youbike_data_202403.csv` | NTU filtered data | ~400K+ | March 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202404.csv` | NTU filtered data | ~400K+ | April 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202405.csv` | NTU filtered data | ~400K+ | May 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202406.csv` | NTU filtered data | ~400K+ | June 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202409.csv` | NTU filtered data | ~400K+ | September 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202410.csv` | NTU filtered data | ~400K+ | October 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202411.csv` | NTU filtered data | ~400K+ | November 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202412.csv` | NTU filtered data | ~400K+ | December 2024 | NTU-related YouBike transactions |
| `ntu_youbike_data_202501.csv` | NTU filtered data | ~400K+ | January 2025 | NTU-related YouBike transactions |

#### 📊 Station Flow Analysis (`/station_flow/`)
| File Name | Description | Records | Period | Content |
|-----------|-------------|---------|--------|---------|
| `station_flow_202403.csv` | Hourly flow data | ~40K+ | March 2024 | Station × Date × Hour flow matrix |
| `station_flow_202404.csv` | Hourly flow data | ~40K+ | April 2024 | Station × Date × Hour flow matrix |
| `station_flow_202405.csv` | Hourly flow data | ~40K+ | May 2024 | Station × Date × Hour flow matrix |
| `station_flow_202406.csv` | Hourly flow data | ~40K+ | June 2024 | Station × Date × Hour flow matrix |
| `station_flow_202409.csv` | Hourly flow data | ~40K+ | September 2024 | Station × Date × Hour flow matrix |
| `station_flow_202410.csv` | Hourly flow data | ~40K+ | October 2024 | Station × Date × Hour flow matrix |
| `station_flow_202411.csv` | Hourly flow data | ~40K+ | November 2024 | Station × Date × Hour flow matrix |
| `station_flow_202412.csv` | Hourly flow data | ~40K+ | December 2024 | Station × Date × Hour flow matrix |
| `station_flow_202501.csv` | Hourly flow data | ~40K+ | January 2025 | Station × Date × Hour flow matrix |

**Station Flow Schema:**
- `station`: Station name
- `date`: Date (YYYY-MM-DD)
- `hour`: Hour (0-23)
- `borrow_count`: Number of borrows
- `return_count`: Number of returns

**Station Flow Schema Example:**
| station | date | hour | borrow_count | return_count |
|---------|------|------|--------------|--------------|
| 基隆長興路口 | 2025-01-01 | 1 | 6.0 | 4.0 |

#### 🏢 Station Information
| File Name | Description | Records | Content |
|-----------|-------------|---------|---------|
| `ntu_area_ubike_stations_new.csv` | NTU station info | 75 | Station details with coordinates and capacity |
| `routes_with_sno_clean.csv` | Route information | 5,255 | Station-to-station routes with distances |

**NTU Station Info Schema (`ntu_area_ubike_stations_new.csv`):**
- `sno`: Station number (e.g., 500119047)
- `sna`: Station name (e.g., "YouBike2.0_臺大土木系館")
- `sarea`: Area name (e.g., "臺大公館校區")
- `latitude`: Latitude coordinate (e.g., 25.01761)
- `longitude`: Longitude coordinate (e.g., 121.53844)
- `ar`: Address (e.g., "臺大土木工程學系所南側")
- `sareaen`: English area name (e.g., "NTU Dist")
- `aren`: English address (e.g., "NTU Dept. of Civil Engineering(South)")
- `act`: Active status (0=inactive, 1=active)
- `total`: Total bike capacity (e.g., 30.0)

**NTU Station Info Schema Example (`ntu_area_ubike_stations_new.csv`):**
| sno | sna | sarea | latitude | longitude | ar | sareaen | aren | act | total |
|-----|-----|-------|----------|-----------|----|---------|-----|-----|-------|
| 500119047 | YouBike2.0_臺大土木系館 | 臺大公館校區 | 25.01761 | 121.53844 | 臺大土木工程學系所南側 | NTU Dist | NTU Dept. of Civil Engineering(South) | 0 | 30.0 |

**Route Information Schema (`routes_with_sno_clean.csv`):**
- `origin`: Origin station name (e.g., "YouBike2.0_辛亥復興路口西北側")
- `destination`: Destination station name (e.g., "YouBike2.0_新生南路三段52號前")
- `distance_km`: Distance in kilometers (e.g., 1.143)
- `duration_min`: Estimated travel time in minutes (e.g., 4.3)
- `origin_sno`: Origin station number (e.g., 500101005.0)
- `destination_sno`: Destination station number (e.g., 500101008.0)

**Route Information Schema Example (`routes_with_sno_clean.csv`):**
| origin | destination | distance_km | duration_min | origin_sno | destination_sno |
|--------|-------------|-------------|--------------|------------|-----------------|
| YouBike2.0_辛亥復興路口西北側 | YouBike2.0_新生南路三段52號前 | 1.143 | 4.3 | 500101005.0 | 500101008.0 |

### 📁 `/code/` - Processing Scripts
| File Name | Description | Purpose |
|-----------|-------------|---------|
| `processing_data.py` | Main processing script | Data filtering and flow analysis |
| `merge_ntu_station_and_total.py` | Station merging script | Combine station data |
| `make_file.py` | File generation script | Create processed files |

### 📁 `/temp/` - Temporary Files
Empty directory for temporary processing files.

## Data Processing Pipeline

1. **Raw Data** → **NTU Filtered Data**
   - Filter YouBike transactions related to NTU stations
   - Extract borrow/return records involving NTU area

2. **NTU Data** → **Station Flow Analysis**
   - Group by station, date, and hour
   - Calculate borrow and return counts
   - Create hourly flow matrix

3. **Station Information**
   - Maintain station metadata
   - Route distance calculations
   - Capacity information

## Usage Notes

- All CSV files use UTF-8 encoding
- Date format: YYYY-MM-DD
- Time format: HH:MM:SS
- Coordinates in decimal degrees
- File sizes are approximate and may vary

## Last Updated
2025-01-15

## Credits
Data documentation and structure organized with assistance from Claude AI Assistant.