#!/usr/bin/env python3
"""Regenerate epg.xml (generic 'Live Radio' blocks) for the stations in radio.m3u.
Usage: python3 generate_epg.py [days]   (default 30)"""
import re, sys, datetime as dt
from xml.sax.saxutils import escape

days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
chans = []
for line in open("radio.m3u", encoding="utf-8"):
    if line.startswith("#EXTINF"):
        cid = re.search(r'tvg-id="([^"]*)"', line).group(1)
        name = re.search(r'tvg-name="([^"]*)"', line).group(1)
        logo = re.search(r'tvg-logo="([^"]*)"', line)
        chans.append((cid, name, logo.group(1) if logo else ""))

start = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
fmt = lambda d: d.strftime("%Y%m%d%H%M%S +0000")
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<tv generator-info-name="custom-radio-epg">']
for cid, name, logo in chans:
    out.append(f'  <channel id="{escape(cid)}"><display-name>{escape(name)}</display-name>'
               + (f'<icon src="{escape(logo)}"/>' if logo else "") + "</channel>")
for cid, name, _ in chans:
    for i in range(days):
        a = start + dt.timedelta(days=i); b = a + dt.timedelta(days=1)
        out.append(f'  <programme start="{fmt(a)}" stop="{fmt(b)}" channel="{escape(cid)}">'
                   f'<title lang="en">{escape(name)} - Live Radio</title>'
                   f'<desc lang="en">Live radio stream.</desc></programme>')
out.append("</tv>")
open("epg.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"{len(chans)} channels, {days} days -> epg.xml")
