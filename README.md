# roars.dev
Roars Website: [roars.dev](https://roars.dev)
[Roars Wiki](https://github.com/dynaroars/dynaroars.github.io/wiki)
  - [Stats about GMU CS](https://github.com/dynaroars/dynaroars.github.io/wiki/About-GMU)
  - [Vietnamese CS Profs in the US](https://github.com/dynaroars/dynaroars.github.io/wiki/Viet-CS-Profs-US)
  - [Culture of Roars Lab](https://github.com/dynaroars/dynaroars.github.io/wiki/Answers-to-Ph.D-Advisor-Guide)

## Private project ideas

Run `node _scripts/build-project-ideas.cjs` (requires Node.js, npm, Pandoc,
and internet access on the first run). This creates a starter `project-ideas.md`
and a random password in `.project-ideas-password`, then builds the encrypted
`project-ideas.html` using [StatiCrypt](https://github.com/robinmoisson/staticrypt).

Edit the Markdown and rerun the command after each change. Read the local
password file to get the shared password; replace it with a long password and
rebuild to change it. Keep backups of both private files outside this public
repository. Both files are ignored by Git and excluded from the Pages build;
never force-add them. Commit the encrypted HTML, builder, and configuration.
The published page is `/project-ideas.html` and requests no search indexing.
