## Stress Tester App Container

### Purpose

 This container is simply a container around the [stress application](http://people.seas.harvard.edu/~apw/stress/).
 When the container is started, it will call the application with parameters provided via environment variables.


### The INSTRUCTIONS Environment Variable

 The application reads the INSTRUCTIONS variable and attempts to convert it to JSON. 
 The JSON document needs an instructions segment and play_mode segment.

#### Examples

Single ordered run
 - `stress --cpu 1 --timeout 10s --quiet`
 - `sleep 30`

 ```
 {
  "instructions": [
    {
      "cmd": "stress",
      "switches": {
        "--cpu": 1,
        "--timeout": "10s"
      },
      "flags": [
        "--quiet"
      ],
      "args": []
    },
    {
      "cmd": "sleep",
      "args": [
        "30"
      ]
    }
  ],
  "play_mode": "single"
}
```

Repeated ordered run
 - `stress --cpu 4 --vm 3 --timeout 5m --verbose`
 - `sleep 10`

 ```
 {
  "instructions": [
    {
      "cmd": "stress",
      "switches": {
        "--cpu": "4",
        "--vm": "3"
        "--timeout": "5m"
      },
      "flags": [
        "--verbose"
      ],
      "args": []
    },
    {
      "cmd": "sleep",
      "args": [
        "30"
      ]
    }
  ],
  "play_mode": "repeat"
}
```

Single shuffle run
 - `stress --cpu 4 --vm 3 --timeout 5m --verbose`
 - `stress --cpu 1 --timeout 10s --quiet`
 - `sleep 30`
 - `sleep 10`

 ```
 {
  "instructions": [
    {
      "cmd": "stress",
      "switches": {
        "--cpu": "4",
        "--vm": "3"
        "--timeout": "5m"
      },
      "flags": [
        "--verbose"
      ],
      "args": []
    },
    {
      "cmd": "stress",
      "switches": {
        "--cpu": 1,
        "--timeout": "10s"
      },
      "flags": [
        "--quiet"
      ],
      "args": []
    },
    {
      "cmd": "sleep",
      "args": [
        "30"
      ]
    },
    {
      "cmd": "sleep",
      "args": [
        "10"
      ]
    }
  ],
  "play_mode": "shuffle"
}
```

Repeated shuffle run
 - `stress --cpu 4 --vm 3 --timeout 5m --verbose`
 - `stress --cpu 1 --timeout 10s --quiet`
 - `sleep 30`
 - `sleep 10`

 ```
 {
  "instructions": [
    {
      "cmd": "stress",
      "switches": {
        "--cpu": "4",
        "--vm": "3"
        "--timeout": "5m"
      },
      "flags": [
        "--verbose"
      ],
      "args": []
    },
    {
      "cmd": "stress",
      "switches": {
        "--cpu": 1,
        "--timeout": "10s"
      },
      "flags": [
        "--quiet"
      ],
      "args": []
    },
    {
      "cmd": "sleep",
      "args": [
        "30"
      ]
    },
    {
      "cmd": "sleep",
      "args": [
        "10"
      ]
    }
  ],
  "play_mode": "repeat_shuffle"
}
```