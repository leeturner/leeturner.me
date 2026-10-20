# Hugo project for leeturner.me

This is the [Hugo](https://gohugo.io) used to generate [leeturner.me](https://leeturner.me).  The site is served from Github Pages and built using Github Actions.

## Theme

The site uses its own theme in `themes/leeturner`, kept in this repo. Layouts live in `themes/leeturner/layouts`,
styles in `themes/leeturner/assets/css/main.css` and the small amount of JavaScript (theme toggle, giscus and the
projects filter) in `themes/leeturner/assets/js/site.js`.

The projects page is generated from `data/projects.yaml`. Add a project there and give it tags; any tag used by
two or more projects becomes a filter button.

Run it locally with `hugo server` (Hugo 0.146 or newer).
