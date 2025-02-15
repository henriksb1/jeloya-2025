interface Mindwave {
    timestamp: string;
    poor_signal: number;
    raw_value: number;
    attention: number;
    meditation: number
    blink: number;
    waves: Waves;
    direction: number;
}

interface Waves {
    delta: number;
    theta: number;
    "low-alpha": number;
    "high-alpha": number;
    "low-beta": number;
    "high-beta": number;
    "low-gamma": number;
    "mid-gamma": number;
}

