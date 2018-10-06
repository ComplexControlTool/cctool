CCTool
======

**Complex Control Tool** is used for building and analysing causal models of your system. Typically, the causal models are based on Fuzzy Cognitive Maps (FCM) and built in a participatory manner with a range of stakeholders.

The following documentation provides an overview on how to build and run the project.

Quick Links:

*  [Directory Layout](#layout)
*  [Prerequisites](#prerequisites)
*  [Installation Guide](#installation)
*  [Running the Project](#runapp)
*  [Clean-up](#cleanup)

## <a name="layout"></a> Directory Layout

```bash
cctool/
├── AUTHORS
├── LICENSE
├── MANIFEST.in
├── backend
│   ├── app.yaml
│   ├── appengine_config.py
│   ├── cctool
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── graphcontrol
│   │   │   ├── Controllability.py
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── static
│   │   │   └── cctool
│   │   │       ├── css
│   │   │       │   ├── bootstrap.min.css
│   │   │       │   ├── font-awesome.min.css
│   │   │       │   ├── home.css
│   │   │       │   ├── other.css
│   │   │       │   └── pace.css
│   │   │       ├── fancybox
│   │   │       │   ├── blank.gif
│   │   │       │   ├── fancybox_loading.gif
│   │   │       │   ├── fancybox_loading@2x.gif
│   │   │       │   ├── fancybox_overlay.png
│   │   │       │   ├── fancybox_sprite.png
│   │   │       │   ├── fancybox_sprite@2x.png
│   │   │       │   ├── jquery.fancybox-v=2.1.5.css
│   │   │       │   └── jquery.fancybox.pack-v=2.1.5.js
│   │   │       ├── fonts
│   │   │       │   ├── FontAwesome.otf
│   │   │       │   ├── fontawesome-webfont.eot
│   │   │       │   ├── fontawesome-webfont.svg
│   │   │       │   ├── fontawesome-webfont.ttf
│   │   │       │   ├── fontawesome-webfont.woff
│   │   │       │   └── fontawesome-webfont.woff2
│   │   │       ├── images
│   │   │       │   ├── header.png
│   │   │       │   ├── portfolio
│   │   │       │   │   ├── casestudies.jpg
│   │   │       │   │   ├── contactus.jpg
│   │   │       │   │   ├── research.jpg
│   │   │       │   │   └── whentouse.jpg
│   │   │       │   ├── screenshots
│   │   │       │   │   ├── screen1.png
│   │   │       │   │   └── screen2.png
│   │   │       │   ├── sponsors
│   │   │       │   │   ├── sponsor01.png
│   │   │       │   │   ├── sponsor02.png
│   │   │       │   │   ├── sponsor03.png
│   │   │       │   │   └── sponsor04.png
│   │   │       │   ├── team
│   │   │       │   │   ├── alexandrapenn.jpg
│   │   │       │   │   ├── davidlloyd.jpg
│   │   │       │   │   ├── nicholaselia.jpg
│   │   │       │   │   └── sotirismoschoyiannis.jpg
│   │   │       │   ├── website-arrows.png
│   │   │       │   └── zoom.png
│   │   │       └── js
│   │   │           ├── bootstrap.min.js
│   │   │           ├── d3.min.js
│   │   │           ├── home.js
│   │   │           ├── html5shiv.js
│   │   │           ├── jquery-1.10.2.min.js
│   │   │           ├── jquery-migrate-1.2.1.min.js
│   │   │           ├── jquery.easing.1.3.js
│   │   │           ├── jsnetworkx.js
│   │   │           ├── other.js
│   │   │           └── pace.js
│   │   ├── templates
│   │   │   └── cctool
│   │   │       ├── base.html
│   │   │       ├── site_home.html
│   │   │       ├── user_invalid.html
│   │   │       ├── user_loggedin.html
│   │   │       ├── user_login.html
│   │   │       ├── user_logout.html
│   │   │       ├── user_register.html
│   │   │       └── user_register_success.html
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── cctoolapp
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── wsgi.py
│   ├── logs
│   │   ├── webapp.log.dg
│   │   └── webapp.log.wf
│   ├── manage.py
│   ├── requirements-vendor.txt
│   ├── requirements.txt
│   └── templates
│       └── admin
│           ├── base_site.html
│           └── index.html
├── docker
│   ├── Dockerfile_backend
│   ├── Dockerfile_frontend
│   ├── database
│   │   └── postgres_restore
│   ├── docker-compose.override.yml
│   ├── docker-compose.yml
│   ├── docker_cleanup.sh
│   ├── docker_cleanup_custom_images_containers.sh
│   ├── docker_create_custom_images.sh
│   ├── docker_remove_everything_docker.sh
│   ├── docker_run_development_mode.sh
│   ├── docker_stats.sh
│   ├── docker_stop_development_mode.sh
│   ├── logo.sh
│   ├── startup_backend_dev.sh
│   ├── startup_frontend_dev.sh
│   └── tmux
│       └── cctool-dev.yml
├── frontend
│   ├── bower.json
│   ├── e2e
│   │   ├── main.po.js
│   │   └── main.spec.js
│   ├── gulp
│   │   ├── build.js
│   │   ├── conf.js
│   │   ├── e2e-tests.js
│   │   ├── inject.js
│   │   ├── scripts.js
│   │   ├── server.js
│   │   ├── unit-tests.js
│   │   └── watch.js
│   ├── gulpfile.js
│   ├── karma.conf.js
│   ├── package.json
│   ├── protractor.conf.js
│   └── src
│       ├── app
│       │   ├── app.api.js
│       │   ├── app.config.js
│       │   ├── app.constants.js
│       │   ├── app.controller.js
│       │   ├── app.module.js
│       │   ├── app.route.js
│       │   ├── app.run.js
│       │   ├── app.values.js
│       │   ├── cctool
│       │   │   ├── cctool.config.js
│       │   │   ├── cctool.module.js
│       │   │   ├── cctool.run.js
│       │   │   ├── components
│       │   │   │   ├── components.module.js
│       │   │   │   ├── control-nodes-analysis
│       │   │   │   │   ├── control-nodes
│       │   │   │   │   │   ├── control-nodes.controller.js
│       │   │   │   │   │   ├── control-nodes.css
│       │   │   │   │   │   ├── control-nodes.html
│       │   │   │   │   │   └── dialogs
│       │   │   │   │   │       ├── graph.compare.html
│       │   │   │   │   │       ├── graph.fullscreen.html
│       │   │   │   │   │       ├── graph.help.html
│       │   │   │   │   │       └── graph.key.html
│       │   │   │   │   ├── control-nodes-analysis.controller.js
│       │   │   │   │   ├── control-nodes-analysis.module.js
│       │   │   │   │   └── stems
│       │   │   │   │       ├── dialogs
│       │   │   │   │       │   ├── stems.fullscreen.html
│       │   │   │   │       │   ├── stems.help.html
│       │   │   │   │       │   └── stems.key.html
│       │   │   │   │       ├── stems.controller.js
│       │   │   │   │       ├── stems.css
│       │   │   │   │       └── stems.html
│       │   │   │   ├── graph
│       │   │   │   │   ├── graph.controller.js
│       │   │   │   │   ├── graph.css
│       │   │   │   │   ├── graph.html
│       │   │   │   │   ├── graph.module.js
│       │   │   │   │   ├── graph.toast.controller.js
│       │   │   │   │   ├── graph.toast.html
│       │   │   │   │   └── templates
│       │   │   │   │       ├── graph-actions.html
│       │   │   │   │       ├── graph.control-nodes.html
│       │   │   │   │       ├── graph.node-updownstream.html
│       │   │   │   │       └── graph.overview.html
│       │   │   │   ├── graphs
│       │   │   │   │   ├── graphs.controller.js
│       │   │   │   │   ├── graphs.css
│       │   │   │   │   ├── graphs.html
│       │   │   │   │   ├── graphs.module.js
│       │   │   │   │   └── templates
│       │   │   │   │       ├── expandable-graph-card
│       │   │   │   │       │   ├── expandable-graph-card.css
│       │   │   │   │       │   └── expandable-graph-card.html
│       │   │   │   │       ├── graph-actions.html
│       │   │   │   │       └── photo-graph-card
│       │   │   │   │           ├── photo-graph-card.css
│       │   │   │   │           └── photo-graph-card.html
│       │   │   │   ├── info
│       │   │   │   │   └── dialogs
│       │   │   │   │       ├── info.css
│       │   │   │   │       └── info.html
│       │   │   │   ├── menu
│       │   │   │   │   ├── menu.controller.js
│       │   │   │   │   ├── menu.css
│       │   │   │   │   ├── menu.html
│       │   │   │   │   └── menu.module.js
│       │   │   │   ├── node-updownstream-analysis
│       │   │   │   │   ├── node-updownstream-analysis.controller.js
│       │   │   │   │   ├── node-updownstream-analysis.css
│       │   │   │   │   ├── node-updownstream-analysis.html
│       │   │   │   │   └── node-updownstream-analysis.module.js
│       │   │   │   └── toolbar
│       │   │   │       ├── toolbar.controller.js
│       │   │   │       ├── toolbar.css
│       │   │   │       ├── toolbar.html
│       │   │   │       └── toolbar.module.js
│       │   │   ├── directives
│       │   │   │   ├── directives.module.js
│       │   │   │   ├── jsnxStems
│       │   │   │   │   ├── jsnxStems.directive.js
│       │   │   │   │   └── jsnxStems.module.js
│       │   │   │   └── visNetwork
│       │   │   │       ├── visNetwork.directive.js
│       │   │   │       └── visNetwork.module.js
│       │   │   ├── filters
│       │   │   │   └── dateString.filter.js
│       │   │   ├── layouts
│       │   │   │   ├── cctool-layout.css
│       │   │   │   └── cctool-layout.html
│       │   │   ├── old
│       │   │   │   ├── graph.html
│       │   │   │   ├── graph.info.html
│       │   │   │   └── graphs
│       │   │   │       ├── graphs.compare.html
│       │   │   │       ├── graphs.config.js
│       │   │   │       ├── graphs.controller.js
│       │   │   │       ├── graphs.css
│       │   │   │       ├── graphs.grid.html
│       │   │   │       ├── graphs.module.js
│       │   │   │       ├── graphs.new
│       │   │   │       │   ├── dialogs
│       │   │   │       │   │   ├── graph.new.addEdge.html
│       │   │   │       │   │   └── graph.new.addNode.html
│       │   │   │       │   ├── graphs.new.config.js
│       │   │   │       │   ├── graphs.new.controller.js
│       │   │   │       │   ├── graphs.new.create.controller.js
│       │   │   │       │   ├── graphs.new.create.html
│       │   │   │       │   ├── graphs.new.css
│       │   │   │       │   ├── graphs.new.filter.js
│       │   │   │       │   ├── graphs.new.html
│       │   │   │       │   ├── graphs.new.import.controller.js
│       │   │   │       │   ├── graphs.new.import.html
│       │   │   │       │   ├── graphs.new.module.js
│       │   │   │       │   ├── graphs.new.old.html
│       │   │   │       │   └── graphs.new.update.html
│       │   │   │       ├── graphs.tabs.html
│       │   │   │       └── graphs.toolbar-extension.html
│       │   │   ├── pages
│       │   │   │   ├── dashboard
│       │   │   │   │   ├── dashboard.controller.js
│       │   │   │   │   ├── dashboard.css
│       │   │   │   │   ├── dashboard.html
│       │   │   │   │   ├── dashboard.module.js
│       │   │   │   │   └── dashboard.route.js
│       │   │   │   ├── graph-manager
│       │   │   │   │   ├── graph-editor
│       │   │   │   │   │   ├── create
│       │   │   │   │   │   │   ├── graph-editor.create.controller.js
│       │   │   │   │   │   │   └── graph-editor.create.html
│       │   │   │   │   │   ├── dialogs
│       │   │   │   │   │   │   ├── graph.new.addEdge.html
│       │   │   │   │   │   │   └── graph.new.addNode.html
│       │   │   │   │   │   ├── graph-editor.controller.js
│       │   │   │   │   │   ├── graph-editor.css
│       │   │   │   │   │   ├── graph-editor.filter.js
│       │   │   │   │   │   ├── graph-editor.module.js
│       │   │   │   │   │   ├── graph-editor.new.html
│       │   │   │   │   │   ├── graph-editor.route.js
│       │   │   │   │   │   ├── graph-editor.update.html
│       │   │   │   │   │   ├── import
│       │   │   │   │   │   │   ├── graph-editor.import.controller.js
│       │   │   │   │   │   │   └── graph-editor.import.html
│       │   │   │   │   │   ├── moved_home.html
│       │   │   │   │   │   └── update
│       │   │   │   │   │       ├── graph-editor.update.controller.js
│       │   │   │   │   │       └── graph-editor.update.html
│       │   │   │   │   ├── graph-manager.controller.js
│       │   │   │   │   ├── graph-manager.css
│       │   │   │   │   ├── graph-manager.html
│       │   │   │   │   ├── graph-manager.module.js
│       │   │   │   │   ├── graph-manager.route.js
│       │   │   │   │   └── templates
│       │   │   │   │       ├── graph-manager.graph.html
│       │   │   │   │       └── graph-manager.graphs.html
│       │   │   │   └── pages.module.js
│       │   │   └── services
│       │   │       ├── colours
│       │   │       │   ├── colours.cctool.service.js
│       │   │       │   ├── colours.colorbrewer.service.js
│       │   │       │   └── colours.module.js
│       │   │       ├── graph
│       │   │       │   ├── graph.module.js
│       │   │       │   └── graph.service.js
│       │   │       ├── graphs
│       │   │       │   ├── graphs.module.js
│       │   │       │   └── graphs.service.js
│       │   │       ├── jsnx
│       │   │       │   ├── jsnx.module.js
│       │   │       │   └── jsnx.service.js
│       │   │       ├── navigation
│       │   │       │   ├── navigation.module.js
│       │   │       │   └── navigation.service.js
│       │   │       ├── services.module.js
│       │   │       └── settings
│       │   │           ├── settings.module.js
│       │   │           └── settings.service.js
│       │   ├── components
│       │   │   └── components.module.js
│       │   ├── core
│       │   │   ├── core.module.js
│       │   │   ├── filters
│       │   │   │   └── core.filters.js
│       │   │   ├── layouts
│       │   │   │   └── basic.html
│       │   │   └── services
│       │   │       ├── api-resolver.service.js
│       │   │       ├── md-theme-colors.js
│       │   │       └── utils.service.js
│       │   ├── data
│       │   │   ├── demo
│       │   │   │   ├── demo.json
│       │   │   │   ├── demo1.json
│       │   │   │   └── demo2.json
│       │   │   └── empty
│       │   │       └── empty.json
│       │   ├── directives
│       │   │   ├── directives.module.js
│       │   │   ├── fileUpload
│       │   │   │   ├── fileUpload.directive.css
│       │   │   │   ├── fileUpload.directive.js
│       │   │   │   ├── fileUpload.module.js
│       │   │   │   └── fileUpload.template.html
│       │   │   └── md-stepper
│       │   │       ├── md-stepper.directive.css
│       │   │       └── md-stepper.directive.js
│       │   ├── index.css
│       │   └── pages
│       │       └── pages.module.js
│       ├── assets
│       │   ├── css
│       │   │   ├── ie-disabled-transitions.css
│       │   │   ├── ie10+-disabled-transitions.css
│       │   │   └── theme-styles.css
│       │   └── images
│       │       ├── graph.png
│       │       └── visjs
│       │           └── network
│       │               ├── add.svg
│       │               ├── back.svg
│       │               ├── close.svg
│       │               ├── downArrow.svg
│       │               ├── edit.svg
│       │               ├── leftArrow.svg
│       │               ├── minus.svg
│       │               ├── plus.svg
│       │               ├── remove.svg
│       │               ├── rightArrow.svg
│       │               ├── upArrow.svg
│       │               └── zoomExtends.svg
│       ├── favicon.ico
│       └── index.html
└── tree.txt

88 directories, 288 files
```

## <a name="prerequisites"></a> Prerequisites

Below are the main technologies used for this project. Take some time to familiarise yourself.

[Homebrew][2]: (for Mac users) An open source software package management system that simplifies the installation of software on MacOS. Highly recommended.

[Docker][3]: Docker is the world’s leading software containerization platform. Chosen to run the development environment in (tested with Docker version 18.06.0-ce, build 0ffa825).

[Docker-compose][4]: Compose is a tool for defining and running multi-container Docker applications (tested with docker-compose version 1.22.0, build f46880f)

[Tmux][5]: Tmux is a terminal multiplexer that lets you switch easily between several programs in one terminal, detach them (while still running in the background) and reattach them to a different terminal (tested with tmux 2.6).

[Tmuxinator][6]: Create and manage tmux sessions easily (tested with tmuxinator 0.10.0).

## <a name="installation"></a> Installation Guide

This repository will build a dockertised development environment out of your [CCTool][1]
repository.

### Instructions for MAC OS X

#### Required packages

* Make sure you have Command Line Tools for Mac OS X installed, by typing the following in a terminal window:

	```bash
	$ xcode-select --install
	``` 

* To install Homebrew, type the following in a terminal window:

	```bash
	$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	``` 

* To install Docker, go to [this link][7] and install Docker CE for Mac (Stable).

* To install Tmux, type the follwoing in a terminal window:

	```bash
	$ brew install tmux
	```

* To install Tmuxinator, type the following in a terminal window:

	```bash
	$ brew install ruby
	$ gem install tmuxinator
	```

#### Prepare / Setup your machine

##### Set up Environment Variables

The tmuxinator setup assumes you have an envrionment variable set up in your system. It expects a `CCTOOL` variable that points to the [CCTool][1] repo path.

There are differnet ways to add environment variables on your machine, but I would recommend to edit the user's bash profile which can be found at `~/.bash_profile`.

* Open the file, using your terminal type the following:

	```bash
	$ open ~/.bash_profile 
	```

* At the end of the file append the following line (replace [/path/to/CCTOOL/cloned/repo] with your [CCTool][1] cloned repo path):

	`export CCTOOL=[/path/to/CCTOOL/cloned/repo]`

* Save the file and restart terminal (or execute `source ~/.bash_profile`). You should be good to go!

Note: To avoid any problems with paths that include spaces, always use `"$CCTOOL"` as your shortcut rather than `$CCTOOL `.

#### Set up Tmuxinator Project

##### Using Tmuxinator new project command

Create a new tmuxinator project by using the following command:

```bash
$ tmuxinator new [project]
```

This will create a [project].yml tmuxinator file under your tmuxinator directory (on Mac usually it can be found at `/Users/[user]/.config/tmuxinator`).

You can rename **[project]** to **cctool-dev** and copy the contents of the file: `[repo]/docker/tmux/cctool-dev.yml`

##### Copying Tmuxinator file

Otherwise, you can just copy the file `[repo]/docker/tmux/cctool-dev.yml` to your tmuxinator directory (`/Users/[user]/.config/tmuxinator/[copy_here]`).

##### Verify Tmuxinator project

To verify installation just run the following command and make sure **cctool-dev** is included:

```bash
$ tmuxinator list
```

## <a name="runapp"></a> Running the Project

Assuming all steps are successfully completed from the [Installation Guide](#installation) section, type the following in a terminal window:

```bash
$ tmuxinator start cctool-dev
```

This command will create and start all the required Docker images/containers for your environment. Progress of the setup can be found in Tmuxinator screen 2. If all are successfully installed/run then CCTool should be available at `http://localhost`.

### Switching branches

Everytime you run the dev-env, it will try and get any new updates for the project (package updates, database migrations etc). So it is safer to kill the current running process of the project before switching branches.

It is then advisable to always run (if you are already running dev-env):

```bash
$ tmuxinator stop cctool-dev
```

and then: 

```bash
$ tmuxinator start cctool-dev
```

## <a name="cleanup"></a> Clean-up

Current project will use Docker containers, images and volumes. Check out [this][8] handy cheat sheet on how to clean-up after you finished.

[1]: https://github.com/ComplexControlTool/cctool.git
[2]: https://brew.sh
[3]: https://www.docker.com/what-docker
[4]: https://docs.docker.com/compose/
[5]: https://tmux.github.io
[6]: https://github.com/tmuxinator/tmuxinator
[7]: https://store.docker.com/editions/community/docker-ce-desktop-mac?tab=description
[8]: https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes