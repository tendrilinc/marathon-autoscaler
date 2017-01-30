#!/usr/bin/env bash
eval $(minimesos info | tail -n +3)
curl http://$(docker-machine ip default):8080/v2/apps
python scripts/render_template.py tests/minimesos/marathon-autoscaler-app-def.json -o autoscaler-app.json
# python scripts/deploy_to_marathon.py autoscaler-app.json --marathon-uri http://$(docker-machine ip default):8080
minimesos install --marathonFile autoscaler-app.json