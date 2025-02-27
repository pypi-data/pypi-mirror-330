#!/bin/bash


reGit_real=$(realpath $reGit)
pwd_real=$(realpath $PWD)
thisdir_rel=${pwd_real#$reGit_real}



function autocopy()
{
    #@ Add auto-copy statement in target export.sh and execute it
    #@
    #@ ---------------------------------
    #@ Last Update: @2025-02-18 13:02:03
    target_file=$1
    target_dir=$(dirname $target_file)
    bname=$(basename $target_file)

    if [[ -z $(grep -P "$bname .*$thisdir_rel;" $target_dir/export.sh) ]]; then
        echo "if [[ -e \$reGit$thisdir_rel ]]; then cp $bname \$reGit$thisdir_rel; fi" >> $target_dir/export.sh
    fi
    (cd $target_dir && ./export.sh)
    # cp $target_file .
}


autocopy $reGit/lasset/rdee-python/Export/libargparse.py
