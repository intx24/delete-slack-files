#!/bin/bash
chmod +x ./ecr_login.sh
./ecr_login.sh

chmod +x ./build.sh
./build.sh

chmod +x ./push_container
./push_container.sh
