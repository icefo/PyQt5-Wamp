#!/usr/bin/env bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

crossbar_config_path="${dir}/crossbar_config"

echo ${crossbar_config_path}

crossbar start --cbdir "${crossbar_config_path}"
