# Changelog

<!--next-version-placeholder-->

## v1.3.0 (2025-02-28)

### Feature

* Changed the nosnap command to now install snap when it doesn't detect it, turning it into getsnap. ([`ecca170`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/ecca170539618476b36e950deda8fa1eda05be17))
* Added a check for nosnap.pref and removes it if it sees it. ([`6f6799f`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/6f6799f4d19874a3f3b9baf849df5b893858c923))

### Fix

*  changed run command to sudo command ([`fc3a948`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/fc3a948b9a2ac3ce79622bbba102e6ca8a3ea10a))
*  removed tkinter sneaking into the file ([`32a908f`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/32a908f639b5381e1b8b35c78c71679d2e4792ac))
*  Put the final touches on the try except. And moved the sudo apt update outside of the try. ([`8209cdc`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/8209cdc6db336cfc71307ac8bed76fb7569dbea1))
*  check if snap and nosnap exists and what to do in install_snap, should be fully finished now. ([`3052bf8`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/3052bf8f5ff635407af5c8faba9d3ebce08f4d86))
* Updated the edwh tool minimum version requirement and changed os.system to edwh.is_installed ([`b9f087a`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/b9f087a5858a76da4dc6a6f5baeb7bf3f8a7bada))

## v1.2.1 (2024-09-03)

### Fix

* Use current user ID instead of hard-coding on 1000 ([`8d2f41c`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/8d2f41cf98a58e623f95661026c29cc982186a42))

## v1.2.0 (2024-07-25)



## v1.2.0-beta.1 (2024-07-25)

### Feature

* `unmount-all` option to (temporarily) unmount everything ([`f36456d`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/f36456d064fe349d799cd64432ad98d45742d192))

### Fix

* Apply gid and uid map when mounting by default ([`341af80`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/341af80aad97f9bde716a9d672a2039ec1d4faad))

## v1.1.2 (2024-07-22)

### Fix

* Indentation error ([`bfda2d7`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/bfda2d76fb7adfda377b1919225131419b5f3114))

## v1.1.1 (2024-07-12)

### Fix

* Slightly improved readable formatting for `ew mp.mounts` ([`5fc1a35`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/5fc1a35cb50d4ed6448790d1421dcfc8d1a15614))

### Documentation

* Manually fix changelog ([`f64ec4c`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/f64ec4c801b6df5e1708fe5e177cb7bdfe8b9c41))

## v1.1.0 (2024-07-12)

### Feature

* Allow edwh to manage mp mounts, so we can do `remount` if mp loses the mounts ([`8b5c5ae`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/8b5c5aee3d5b520de5b4a76f6ded207782cc68ba))
* Add `ew mp.mount` which stores mounts in order to do `ew mp.remount` later on ([`a208679`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/a208679af06b411d81510c47c09ba81edce6feb3))

### Fix

* Improve typing (mypy) ([`5554a42`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/5554a42ca9902921c254a4e20c5a909dce049bbb))
* Improved remote execution (worked only locally before) - requires edwh>=0.43 ([`0eab701`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/0eab701b70a83c7d4e30a9d5cf61ff11349985fd))


## v1.0.3 (2024-07-04)

### Fix

* Update way too long command suggestion at the end of `prepare-multipass` to simply remote.prepare-generic-server (since that's probably your next step) ([`da20a6e`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/da20a6e6d465c14b1f0d6ba389c649f79f39fd81))
* Minor improvements in typing, docs, refactoring ([`b64056b`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/b64056bffdbf6b9e0dd77ae3f0eb7bcad9700a9d))

## v1.0.2 (2024-04-12)

### Fix

* Use require_sudo for improved password prompting + general refactoring ([`b2fd319`](https://github.com/educationwarehouse/edwh-multipass-plugin/commit/b2fd3192097800832254fab9cd691c20acd29f66))

## v1.0.1 (2023-05-01)

