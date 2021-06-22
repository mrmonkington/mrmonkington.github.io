Title: How to build an only-slightly-less-than-trivial GTK4 app using Flatpak
Date: 2021-06-18 21:30
Category: HOWTOs
Tags: GTK, Flatpak, meson
Summary: GTK4 is pretty new, and so it's likely that if you want to target it, you'll need to get your head around Flatpak in order to distribute your work. Here, I've taken the GTK4 'custom drawing' example from the GTK docs and wrapped it in a meson and Flatpak example, with a bit of explanation.

GTK4 is pretty new, and so it's likely that if you want to target it, you'll need to get your head around Flatpak in order to distribute your work.

Herein is the [GTK4 'custom drawing' example from the docs](https://developer.gnome.org/gtk4/stable/ch01s04.html) wrapped in a meson and Flatpak example.

<i>(Note, this write up doesn't cover publishing your application... yet)</i>

<dl>
  <dt>App name:</dt>
    <dd>drawing-example
  <dt>App domain:</dt>
    <dd>com.verynoisy <i>This is my domain, make up your own!</i>
  <dt>Build system:</dt>
    <dd>meson + ninja (c.f. configure + make)
</dl>

Dir structure:

```shell
drawing-example/
  source/
    meson.build
    src/
      meson.build
      drawing-example.c
```

Grab the source from the gtk4 docs: https://developer.gnome.org/gtk4/stable/ch01s04.html

Place in `drawing-example/source/src/drawing-example.c`

Edit the source so the app name is `com.verynoisy.drawing-example` on line 182 - this is important to ensure DBus permissions are correct, since Flatpak by default will only grant portal permissions to the bus of the same name as the app.

Install latest flatpak:

```sh
sudo add-apt-repository ppa:alexlarsson/flatpak
sudo apt update
sudo apt install flatpak flatpak-builder
```

Install latest platform and sdk images:

```sh
flatpak install org.gnome.Sdk//master
flatpak install org.gnome.Platform//40
```

Create top level meson build specification:

In `drawing-example/source/meson.build`:

```
project('drawing-example', 'c',
  meson_version: '>= 0.56.0',
  default_options: [
    'warning_level=2',
    'c_std=gnu11',
  ],
)

subdir('src')
```

...and one in the actual source directory:

```
drawing_example_sources = [
  'drawing-example.c',
]

drawing_example_deps = [
  dependency('gtk4', version: '>= 4.0'),
]

executable('drawing-example', drawing_example_sources,
  dependencies: drawing_example_deps, install: true
)
```

(This is needlessly fragmented for a simple project, but you'll need this separation the moment your project gets even vaguely complex.)

Create flatpak manifest so it knows how to invoke your build, etc, in `drawing-example/com.verynoisy.drawing-example.yml`:

```yaml
---
app-id: com.verynoisy.drawing-example
runtime: org.gnome.Platform
runtime-version: '40'
sdk: org.gnome.Sdk
command: drawing-example
finish-args:
  - "--share=ipc"
  - "--socket=x11"
  - "--share=network"
  - "--device=dri"  # for opengl
modules:
  - name: drawing-example
    buildsystem: meson
    sources:
      - type: dir
        path: source
```

Build:

```sh
flatpak-builder --install \
  --user \
  build-dir \
  com.verynoisy.drawing-example.yml \
  com.verynoisy.drawing-example
```

(You can add `--force-clean` if you've just made changes to configs)

This will do this following:

  - Initialise a flatpak build directory with your chosen platform and SDK, in `build-dir`.
  - Run `meson setup --prefix=/app` against the build config on your host machine, but in the sandbox, using the meson version (and other dev tools) provided by the SDK you selected, outputting all build files somewhere in `build-dir` (you don't really need to care where).
  - Sandbox-run `ninja` (c.f. `make`) against those meson build files, producing your binary.
  - Install it all the the right place in the flatpak build-dir, as if it were installed on a real system under `/app` (c.f. `/usr/local/`, etc)

Test:

```sh
flatpak-builder \
  --run --socket=x11 \
  --share=ipc \
  --device=dri \
  build-dir \
  com.verynoisy.drawing-example.yml \
  /app/bin/drawing-example
```

## debugging DBus probs (e.g. can't register, etc)

Listen for all DBus activity
```sh
dbus-monitor --session
```

See what this app tries to do:
```sh
flatpak-builder --run \
  --socket=session-bus \
  --share=network \
  --socket=x11 \
  --share=ipc \
  --device=dri \
  build-dir \
  com.verynoisy.drawing-example.yml \
  /app/bin/drawing-example
```

TODO:

  - Debugging
  - Releasing
  - Drawing the rest of the owl...


