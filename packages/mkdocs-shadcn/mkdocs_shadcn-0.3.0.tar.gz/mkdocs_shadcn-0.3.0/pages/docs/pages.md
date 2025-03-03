---
title: Pages
summary: Metadata configuration
---

Like this page, you can define its title (and subtitle) through front-matter 
configuration.

```yaml
title: Pages # title
summary: Metadata configuration # subtitle
```

## Navigation

In addition, two other attributes may help to configure the sidebar.

```yaml
order: 2 # title
sidebar_title: Navigation title
```

The `order` attribute may help to change the rank of the page in the sidebar (without setting the `nav` setting in `mkdocs.yml`). By default, mkdocs ranks pages through alphebetical order. We keep this behavior if `order` is not set. Let us take this example:

```ini
| a.md ; order not set
| b.md ; order: 42
| c.md ; order: 0
| d.md ; order not set
```

After a first pass we will have

```ini
| a.md ; order: 0
| b.md ; order: 42
| c.md ; order: 0
| d.md ; order: 1
```

So in the sidebar we will get `a.md`, `c.md`, `d.md` and `b.md`.

## SEO

The following attributes are supported for SEO (`<meta>` attributes in the `<head>`).

```yaml
description: Extra page description
keywords: mkdocs,shadcn
author: asiffer
image: https://raw.githubusercontent.com/asiffer/mkdocs-shadcn/refs/heads/master/.github/assets/logo.svg
```