#!/bin/bash
# Copyright (c) 2014 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Licensee has the right to choose one of the above licenses.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
set -xe
readonly SUCCESS=0
readonly FAILURE=1
readonly RHEL_DIST="el"
readonly UBUNTU_DIST="ubuntu"
readonly REDHAT_FILE="/etc/redhat-release"
readonly UBUNTU_FIlE="/etc/os-release"

PACKAGE_NAME="Ceilometer Mellanox SR-IOV inspector"
DIST=""
CEILOMETER_VERSION="6.0.0"
CEILOMETER_RELEASE="0"
ROOT_RPMBUILD="/root/rpmbuild/"
BUILD_DEST="$ROOT_RPMBUILD/BUILD/"
BUILD_TARGET=$(pwd)

function check_dist() {
    if [ -f ${REDHAT_FILE} ]; then
        if grep -q -i "release 6" ${REDHAT_FILE} || grep -q -i "release 7" ${REDHAT_FILE}; then
            DIST=${RHEL_DIST}
        else
            echo "$PACKAGE_NAME Support only CentOS and RedHat Release 6 or 7"
            exit ${FAILURE}
        fi
    elif [ -f ${UBUNTU_FIlE} ]; then
        DIST=${UBUNTU_DIST}
    else
        echo "$PACKAGE_NAME Supports only CentOS 6 and Ubuntu"
        exit ${FAILURE}
    fi
}


function build_rpm(){
    \cp -rf ../.git ../mlnx_libvirt ../README.rst ../setup.py ../setup.cfg $BUILD_DEST
    cp -rf ../README.rst ../setup.py ../setup.cfg $BUILD_DEST
    rpmbuild -ba centos/mlnx_sriov_ceilometer.spec
    cp $ROOT_RPMBUILD/RPMS/x86_64/* $BUILD_TARGET
    cp $ROOT_RPMBUILD/SRPMS/* $BUILD_TARGET

}

function update_deb_version(){
    sed "s/@@VERSION@@/${CEILOMETER_VERSION}/g;s/@@RELEASE@@/${CEILOMETER_RELEASE}/g" debian/changelog.template > debian/changelog
    if [ $? != ${SUCCESS} ] ; then
        echo "Failed to update deb version"
        deb_cleanup
        exit ${FAILURE}
    fi
}

function build_deb(){
    deb_cleanup
    cp -rf ../setup.py ../setup.cfg ../README.rst .
    mkdir -p ceilometer/compute/virt
    cp -rf ../mlnx_libvirt ceilometer/compute/virt/

    update_deb_version
    export DEB_BUILD_OPTIONS=nocheck
    dpkg-buildpackage -b --force-sign
}

function deb_cleanup() {
    echo "Cleaning"
    rm -rf AUTHORS ChangeLog README.rst mlnx_sriov_ceilometer.egg-info setup.cfg setup.py
}


check_dist
if [ $DIST == $RHEL_DIST ]; then
    build_rpm
elif [ $DIST == $UBUNTU_DIST ]; then
    build_deb
fi

echo "Build finished successfully. Build Files are located at: $BUILD_TARGET"

exit ${SUCCESS}
