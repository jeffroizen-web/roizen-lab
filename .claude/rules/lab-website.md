---
description: Standards for the Ace Scout (Roizen Lab) website
---

# Lab Website Standards

## DOM Construction
- All dynamic DOM: use `<template>` + `cloneNode()` + `textContent`
- Use `<template>` + `cloneNode()` + `textContent` exclusively (security hook enforces this)
- Use event delegation for all event handlers (bind to parent elements)

## Accessibility
- All images need descriptive `alt` attributes
- Semantic HTML: `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`
- Color contrast: minimum 4.5:1 ratio (WCAG AA)

## Design System
- Theme: purple-gold (`#3B1F6E` primary / `#C5A336` accent)
- Institution bar: CHOP + CHOP RI on left, Penn Medicine on right
- Mobile breakpoint: 768px
- Font hierarchy follows Ethan Goldberg-style dual header pattern

## Content
- Jeff's voice over Claude's rewrites — use his phrasing verbatim
- Write direct and real — match Jeff's natural voice
- Heading style: short and declarative (e.g., "Low Vitamin D: Cause or Effect?")
