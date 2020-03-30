/**
 * Represents the raw data collected from applicable sources (Twitter, NOAA, USGS, NEWS)
 */
class RawData {
    author: string;
    lat: number;
    lon: number;
    raw_text: string;
    source: string;
    time: string;
}

/**
 * Interface for JSON response body
 * ProcessedData represents the raw data that has been fed through the
 * natural language processing algorithm and returned in the following structure
 */
export interface ProcessedData {
    id: string;
    raw: RawData;
    threat_type: string;
    time: string;
}
