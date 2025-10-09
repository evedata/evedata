#!/bin/bash

set -e

source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde _dlt_loads &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde _dlt_pipeline_state &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde _dlt_version &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde accountingentrytypes &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde clonestates &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde clonestates__skills &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde compressibletypes &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde dogmaeffectcategories &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde expertsystems &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde expertsystems__associated_ship_types &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde expertsystems__skills_granted &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde graphicmaterialsets &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryactivities &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryassemblylines &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryassemblylines__details_per_category &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryassemblylines__details_per_group &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryassemblylines__details_per_type_list &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryinstallationtypes &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industryinstallationtypes__assembly_lines &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__copying__cost &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__copying__time &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__invention__cost &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__invention__time &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__manufacturing__cost &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__manufacturing__material &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__manufacturing__time &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__reaction__material &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__reaction__time &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__research_material__cost &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__research_material__time &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__research_time__cost &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrymodifiersources__research_time__time &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrytargetfilters &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrytargetfilters__category_ids &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde industrytargetfilters__group_ids &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde repackagedvolumes &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde schoolmap &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde schools &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde schools__starting_stations &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde skillplans &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde skillplans__milestones &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde skillplans__skill_requirements &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde skins &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde skins__types &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde stationstandingsrestrictions &&
source dbt_packages/codegen/bash_scripts/base_model_creation.sh raw_hde stationstandingsrestrictions__services
