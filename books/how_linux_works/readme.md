# Big Picture
## Linux 추상화 레벨
* User Processes
  - Graphical User Interface
  - Servers
  - Shell
* Linux Kernel
  - System Calls
  - Process Management
  - Memory Management
  - Device Drivers
* Hardware
  - Processor (CPU)
  - Main Memory (RAM)
  - Disks
  - Network Ports

# Device
## Device 종류
* Block device
  - 비휘발성이며 어떤 순서로도 저장된 데이터에 접근 가능한 스토리지 디바이스
  - Hard disk, floppy disk, CD-ROM
* Character device
  - 물리적 주소를 갖지 않는 스토리지 디바이스
  - I/O가 byte stream으로 이루어진다.
  - Printer, tape drives, serial ports, parallel ports, /dev/null
* Pipe device
* Socket device

# Disks and Filesystems
## Disk의 계층구조
```
Disks -> Partition Table -> Partitions -> Filesystem Data Structures -> File Data
```
* 커널은 각 파티션을 하나의 block device (/dev/sda1)로 표현한다.
* 파티션들의 정보를 담고 있는 것이 partition table이다.

## Partition table 종류
* MBR (Master Boot Record)
* GPT (Globally Unique Identifier Partition Table)

## Filesystem 종류
* ext series (Extended filesystem)
  - ext2: 오랜기간 linux filesystem의 디폴트였다.
  - ext3: 부팅을 빠르게 하고, data integrity를 강화하기 위해 journal feature(filesystem data structure 외부에 작은 cache)을 추가했다.
  - ext4: 증분적 향상과 큰 파일에 대한 서포트, 서브 디렉토리의 수를 강화하였다.
  - ext2를 ext4처럼 mount하는 것은 가능하나, ext4를 ext2처럼 mount하는 것은 불가능
* btrfs (B-tree filesystem)
* FAT filesystem (msdos, vfat, exfat)
  - FAT: File Allocation Table
  - USB, SD card와 같은 flash media들 대부분이 채택하고 있는 filesystem이다.
* XFS
  - Linux 일부 distribution이 채택하고 있는 고성능 filesystem이다.
  - RHEL
* HFS+
  - Apple의 표준 filesystem
* ISO 9660
  - CD-ROM의 표준 filesystem

## LVM (Logical Volume Manager)
기존의 block device -> filesystem의 계층구조가 가지는 단점들을 보완하기 위해 추가된 추상계층이다.

기존의 계층구조는 초기 디스크 설치 이후에 디스크를 업그레이드하거나, 추가 디스크를 설치하거나, 파티션 혹은 파일시스템을 추가할 때 boot loader의 수정, 재부팅, 재마운트 등의 작업이 필요하게 된다.

이것은 디스크 공간 관리의 유연성을 떨어뜨리게 되고, 이러한 문제점들을 해결하기 위해 LVM이 등장하게 된다.

LVM으로 인해 physical volume -> volume group -> logical volume의 계층구조가 만들어졌다.

대부분의 LVM 베이스 시스템은 하나의 PV와 두개의 LV(root and swap)를 가진다.

LV는 block device이며 보통 filesystem 혹은 swap signature를 가지고 있다.

# Kernel Boots
1. BIOS (Basic IO System) or boot firmware loading
2. Run boot loader
3. Kernel initialization
    - CPU inspection
    - Memory inspection
    - Device bus discovery
    - Auxiliary kernel subsystem setup (network and the like)
    - Root filesystem mount
    - Starts a program called *_init_* with a process ID of 1
4. User space start
    - init (systemd)
    - Essential low-level services (udevd, syslogd)
    - Network configuration
    - Mid/high-level services (cron, printing)
    - Login prompts, GUIs, high-level applications

## Kernel parameters
커널을 시작할 때 커널의 행동을 제어할 수 있는 각종 파라미터를 정의할 수 있다.

현재 시스템에 적용된 파라미터를 보려면 cat /proc/cmdline을 실행하면 된다.

커널의 boot parameter를 정의하는 방법은 boot loader 실행 화면에서 일시적으로 정의하던가, 해당 운영체제가 지원하는 영구적 정의방법에 따르면 된다.
(Ubuntu의 경우 /etc/default/grub 파일을 수정함으로써 영구적으로 커널 파라미터를 수정할 수 있다.)

## Boot loaders
* GRUB
* LILO
* SYSLINUX
* LOADLIN
* systemd-boot
* coreboot
* Linux Kernel EFISTUB
* efilinux

# User Space Starts
User space의 시작은 아래와 같은 순서로 진행된다.
1. init (systemd)
2. Essential low-level services (udevd, syslogd)
3. Network configuration
4. Mid/high-level services (cron, printing)
5. Login prompts, GUIs, high-level applications

## init
init이란 user-space 프로그램의 하나로 시스템의 기본적인 service processes를 시작하거나 정지시키기 위한 목적을 지닌다.

### init의 종류
* Sys-V (sys-five)
  - 전통적 init 프로그램으로 RHEL7과 debian8 이전에서 찾아볼 수 있다.
* Upstart
  - 전통적 init 프로그램으로 ubuntu15.04 이전에서 찾아볼 수 있다.
* systemd
  - 현대 linux의 표준 init 프로그램이다.

### systemd
systemd는 *_unit_*단위로 작업을 진행한다.
이때 unit이란 하나의 goal이며, 일련의 작업명령(daemon의 실행 등)을 포함하고 있다.
unit은 다른 unit들을 dependencies로 가질 수 있기에 systemd는 dependency graphs의 계층구조에 따라 unit을 activate 해나간다.

unit에는 대표적으로 다음의 4가지 타입이 존재한다.
1. Service units
2. Target units
3. Socket units
4. Mount units

해당 unit이 무엇이고 어떻게 실행시키거나, 재실행시켜야 하는지 정의하고 있는 파일이 init file이다. init file은 크게 [Unit], [Service], [Install], [Socket], [Mount], [Automount], [Swap], [Path], [Timer], [Slice] 등의 영역으로 나뉜다. 시스템에 unit을 수동적으로 추가하고 싶을 경우 /etc/systemd/system에 자신이 만든 unit file을 배치시켜놓으면 된다. (mauanl addition: not recommended)
```
# /lib/systemd/system/docker.service
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service containerd.service
Wants=network-online.target
Requires=docker.socket containerd.service

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still    
# exists and systemd currently does not support the cgroup feature set required      
# for containers run by docker
ExecStart=/usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock     
ExecReload=/bin/kill -s HUP $MAINPID
TimeoutSec=0
RestartSec=2
Restart=always

[Install]
WantedBy=multi-user.target
```

```
# 현재의 unit 정보를 습득
$ systemctl list-units

# 대상 unit 정보를 습득
$ systemctl status <unit>

# 대상 unit 시작, 정지, 재시작
$ systemctl start <unit>
$ systemctl stop <unit>
$ systemctl restart <unit>

# unit configuration 파일을 수정했을 경우 재로드
$ systemctl reload <unit>

# 전 unit configuration 파일을 재로드
$ systemctl daemon-reload

# 현재 jobs 정보를 습득
# job: unit의 activate, reactivate and restart
$ systemctl list-jobs
```

* 참고용 man pages
  - systemd.unit
  - systemd.exec
  - systemd.socket
  - systemd.path

# Logging, System Time, Batch jobs, and Users
## Logging
systemd를 사용하는 대부분의 distribution은 journald이라는 systemd 내장 로그 daemon을 이용하여 시스템 로그를 남긴다.
본인의 os가 journal을 쓰고 있는지는 journalctl 커맨드를 실행해보면 알 수 있다.

journald을 쓰지 않는 전통적인 os는 syslogd를 쓴다.

```
# 전체 log 습득
$ journalctl

# 커널 log 습득
$ journalctl -k

# 시간역순 log 습득
$ journalctl -r

# 기타 필터링
# -u: unit
# -S: since
# -U: until
# -g: global regex
# -b: boot
# -p: priority (0: most important ~ 7)
$ journalctl _PID=3454
$ journalctl -u docker.service
$ journalctl -S -4h
$ journalctl -S 06:00:00
$ journalctl -S 2022-05-03 -U 2022-05-04
$ journalctl -S '2022-05-03 07:00:00'
$ journalctl -g <pattern>
$ journalctl -p 3
$ journalctl -p 2..3

# 가장 최근의 boot 로그를 출력
$ journalctl -b -1

# 모든 boot ID를 출력
$ journalctl --list-boots

# _SYSTEMD_UNIT 필드의 모든 값들 출력
$ journalctl -F _SYSTEMD_UNIT

# 모든 필드 출력
$ journalctl -N

# 로그 following
$ journalctl -f
```

* 참고용 man pages
  - journald.conf
  - syslog
  - rsyslog.conf

## Users
kernel 레벨에서 user는 숫자(userid)이지만 user space 관점에서 user는 문자열(username)로 되어있다.
userid와 username을 맵핑하고 있는 파일이 passwd(/etc/passwd)다.
해당 파일은 유저에 대한 7가지 정보를 담고 있다.
```
root:x:0:0:root:/root:/bin/bash
sshd:x:112:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
taeho:x:1000:1000:taeho:/home/taeho:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
```
* username
* encrypted password
  - x: encrypted password는 shadow(/etc/shadow) 파일에 있음
  - *: 로그인 불가능한 user
  - blank: password 없이 로그인 가능한 user
* userid
* groupid
* user's real name
* user's home directory
* user's shell

Linux에는 2가지 특별한 user가 존재한다.
1. superuser
    - 언제나 UID=0, GID=0
2. pseudo user
    - 로그인이 불가능한 user
    - daemon 등이 해당
    - security issue로 생성하는 user

user들은 group에 속하게 되는데, group은 /etc/group 파일에서 관리된다.
Linux는 새로운 user가 생성될 때마다 해당 user의 username과 동일한 group을 생성한다.
```
root:x:0:
ssh:x:114:
landscape:x:115:
lxd:x:116:taeho
systemd-coredump:x:999:
taeho:x:1000:
docker:x:998:taeho
```
* group name
* group password
* groupid
* user list (optional)

본인이 소속되어 있는 group은 groups 커맨드로 알 수 있다.