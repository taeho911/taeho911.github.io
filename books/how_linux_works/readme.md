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