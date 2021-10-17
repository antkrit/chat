# Chat Specification

The key words `MUST`, `MUST NOT`, `REQUIRED`, `SHALL`, `SHALL NOT`, `SHOULD`, `SHOULD NOT`, `RECOMMENDED`,
`NOT RECOMMENDED`, `MAY`, and `OPTIONAL` in this document are to be interpreted as described in
[RFC2119](https://tools.ietf.org/html/rfc2119) only when, they appear in all capitals.

This project is under [MIT](../LICENSE) license

## Github
### Branches
- `main` - master branch, contains the latest stable version of the application
- `dev` - additional branch, it contains all the commits before the release (merge into the main branch)
> any other branches are temporary and MAY be removed soon

### Versioning
This application is versioned using a [Semantic Versioning](https://semver.org/) scheme.
Current version of the application is stored in [package.json](../package.json) file.

The `major`.`minor` portion of the version string (for example 1.1) MUST designate feature set.
The `.patch` portion is for bug fixes.
The functionality of the program version, for example `1.1`, SHOULD be the same as in version `1.1.*`.
Occasionally, non-backwards compatible changes MAY be made in minor versions if impact is considered to be
low relative to the benefit provided.

### Project structure

Folders:
- [config](../config) - SHOULD contain application configuration files
- [documentation](../documentation) - MUST contain anything related to documentation
- [src](../src) - SHOULD contain everything related to the application

## Functionality
Chat is a simple chat website where different people can
communicate with each other.

Anyone can enter the chat or create it without the need to register on the site. 
In this case, the nickname will be generated randomly. Also, the chat may be closed. 
To join such a chat you need to enter a password.
