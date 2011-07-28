#!/usr/bin/env python

from urllib2 import urlopen, HTTPError
from md5 import md5
from re import compile

class colors:
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'
    end = '\033[0m'

ius_base = 'http://dl.iuscommunity.org/pub/ius/'
default_path = 'stable/Redhat'
release = '5'
arch = 'x86_64'

# All of IUS Mirrors
request = urlopen('http://dmirr.iuscommunity.org/project/ius').read()
mirrors = compile('<img src="/themes/default/_img/flags/.*\.png" /> <a href="(.*)">.*</a> - \[').findall(request)

repo = '%s%s/%s/%s' % (ius_base, default_path, release, arch)
response = urlopen(repo).read()
rpms = compile('<a href="(.*\.rpm)">').findall(response)

for rpm in rpms:    
    print '\n%s' % rpm
    print '-' * 75
    filepath = '%s/%s' % (repo, rpm)
    rpmfile = urlopen(filepath).read()
    upstream_md5 = md5(rpmfile).hexdigest()
    print '%-42s - upstream ius' % (colors.green + upstream_md5 + colors.end)

    for mirror in mirrors:
        mirror_repo = '%s%s/%s/%s' % (mirror, default_path, release, arch)
        mirror_filepath = '%s/%s' % (mirror_repo, rpm)
        try:
            rpmfile = urlopen(mirror_filepath).read()
            mirror_md5 = md5(rpmfile).hexdigest()
        except HTTPError as e:
            mirror_md5 = '%s %s' % (e.getcode(), e.msg)

        # visual colors
        if upstream_md5 == mirror_md5:
            color = colors.green
        else:
            color = colors.red

        print '%-42s - %s' % (color + mirror_md5 + colors.end, mirror)
        

        
