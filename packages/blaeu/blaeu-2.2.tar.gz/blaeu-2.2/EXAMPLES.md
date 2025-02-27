# Examples of using Blaeu

For a general introduction, see [the main documentation](README.md) or
[my article at RIPE
Labs](https://labs.ripe.net/Members/stephane_bortzmeyer/creating-ripe-atlas-one-off-measurements-with-blaeu). **Important**:
remember you'll need Atlas credits and an API key. See
[the main documentation](README.md) about that.

## blaeu-reach 

It tests the reachability of the target with ICMP echo packets, like
the traditional `ping`.

The only mandatory argument is an IP address (*not* a domain name).

Basic use, when everything is OK:

```
% blaeu-reach 217.70.184.38                                                       
5 probes reported
Test #78817889 done at 2024-09-06T13:11:02Z
Tests: 15 successful tests (100.0 %), 0 errors (0.0 %), 0 timeouts (0.0 %), average RTT: 90 ms
```

By default, you get 5 probes, and 3 tests per probe (hence the 15 tests).

More probes, but less tests per probe:

```
% blaeu-reach --requested 10 --tests 1 2606:4700::6812:eb44
10 probes reported
Test #78817934 done at 2024-09-06T13:14:47Z
Tests: 10 successful tests (100.0 %), 0 errors (0.0 %), 0 timeouts (0.0 %), average RTT: 23 ms
```

Of course, sometimes, there are problems, so you do not have 100 %
success:

```
% blaeu-reach --requested 200 2001:470:0:149::2
200 probes reported
Test #78817974 done at 2024-09-06T13:18:00Z
Tests: 588 successful tests (98.0 %), 0 errors (0.0 %), 12 timeouts (2.0 %), average RTT: 146 ms
```

To get more details, we will process the existing measurement, asking
to display the faulty probes:

```
% blaeu-reach --requested 200 --measurement-ID 78817974  --by_probe --displayprobes 2001:470:0:149::2
Test #78817974 done at 2024-09-06T13:18:00Z
Tests: 196 successful probes (98.0 %), 4 failed (2.0 %), average RTT: 146 ms
[1006805, 61970, 6890, 7016]
```

You can now search the [Atlas Web site](https://atlas.ripe.net/) to
see what these probes have in common.

There are global options, valid for every Blaeu command, like
`--requested` or ``--measurement-ID`` above, and command-specific options, like `--tests`
above. Calling a command with the `--help` option will give you the
list.

## Probe selection

A great feature of Atlas probes is the ability to select probes based
on various criteria. This is possible with global options.

For network issues, you will typically select based on AS or IP
prefix:

```
% blaeu-reach --requested 10 --as 3215 2001:41d0:404:200::2df6
10 probes reported
Test #78817989 done at 2024-09-06T13:19:26Z
Tests: 30 successful tests (100.0 %), 0 errors (0.0 %), 0 timeouts (0.0 %), average RTT: 57 ms
```

For more political issues, you will probably use the country or the
area (see examples when talking about `blaeu-resolve`).

You can also re-use the probes of a previous measurement with
``--old-measurement`.

## blaeu-traceroute 

Like the traditional traceroute, it displays routers from the probes
to the target (which must be an IP address). By default, you will have to see the results on the
Atlas Web site so you'll probably almost always use the option
`--format` for immediate display:

```
% blaeu-traceroute --requested 3 --format 160.92.168.33
…
Test #78818145 done at 2024-09-06T13:29:11Z

From:  41.136.159.117    23889    MauritiusTelecom, MU
Source address:  192.168.100.90
Probe ID:  64274
1    192.168.100.1    NA    NA    [1.758, 1.456, 1.266]
2    197.226.230.71    23889    MauritiusTelecom, MU    [3.343, 2.863, 2.624]
3    197.224.187.63    23889    MauritiusTelecom, MU    [3.388, 3.81, 2.857]
4    197.226.230.79    23889    MauritiusTelecom, MU    [135.356, 135.622, 135.742]
5    197.226.230.12    23889    MauritiusTelecom, MU    [78.111, 78.315, 78.051]
6    180.87.105.48    6453    AS6453, US    [135.666, 135.546, 135.677]
7    63.243.180.72    6453    AS6453, US    [77.373, 77.451, 78.27]
8    129.250.66.9    2914    NTT-LTD-2914, US    [130.727, 133.305, 134.793]
9    ['*', '*', '*']
10    129.250.7.9    2914    NTT-LTD-2914, US    [334.317, '*', 322.722]
11    129.250.4.188    2914    NTT-LTD-2914, US    [366.291, 371.532, 367.035]
12    129.250.4.174    2914    NTT-LTD-2914, US    [367.325, 369.696, 365.832]
13    128.241.6.223    2914    NTT-LTD-2914, US    [255.407, 257.445, 251.827]
14    10.60.17.199    NA    NA    [282.123, 286.52, 284.159]
15    10.60.17.199    NA    NA    [283.969, 286.804, 285.138]
16    ['*', '*', '*']
17    ['*', '*', '*']
18    ['*', '*', '*']
19    ['*', '*', '*']
20    ['*', '*', '*']
255    ['*', '*', '*']
…
```

It displays the IP address of the router, its AS number and name, its
country, then the three response times. 

By default, it uses UDP packets but you can change, which is useful
for targets that block UDP and/or returned ICMP packets. Here, since
the target is a HTTP server, we use TCP and port 80:

```
% blaeu-traceroute --requested 3 --old-measurement 78818145  --format --protocol TCP --port 80 160.92.168.33
…
Measurement #78818277 Traceroute 160.92.168.33 from probes of measurement #78818145 uses 3 probes
…
From:  41.136.159.117    23889    MauritiusTelecom, MU
Source address:  192.168.100.90
Probe ID:  64274
1    192.168.100.1    NA    NA    [1.764, 0.854, 0.738]
2    197.226.230.71    23889    MauritiusTelecom, MU    [2.936, 2.746, 2.284]
3    197.224.187.63    23889    MauritiusTelecom, MU    [3.159, 3.281, 3.298]
4    197.226.230.81    23889    MauritiusTelecom, MU    [79.637, 79.223, 79.214]
5    197.226.230.0    23889    MauritiusTelecom, MU    [78.875, 79.159, 79.157]
6    180.87.105.48    6453    AS6453, US    [136.319, 135.882, 136.125]
7    ['*', '*', '*']
8    129.250.66.9    2914    NTT-LTD-2914, US    [135.002, 136.063, 135.87]
9    129.250.5.65    2914    NTT-LTD-2914, US    ['*', 137.889, '*']
10    129.250.4.181    2914    NTT-LTD-2914, US    ['*', 454.674, '*']
11    129.250.7.29    2914    NTT-LTD-2914, US    [310.179, 308.374, 306.777]
12    129.250.2.93    2914    NTT-LTD-2914, US    [309.439, 307.089, 319.611]
13    128.241.6.227    2914    NTT-LTD-2914, US    [289.783, 292.489, 290.928]
14    10.60.17.199    NA    NA    ['*', 300.945, 300.237]
15    10.60.17.199    NA    NA    ['*', 300.443, 300.967]
16    160.92.168.33    47957    ING-AS, FR    [275.625, 273.625, 273.543]
```

This time, we have the complete route.

## blaeu-resolve

The DNS resolver of the probes is used to resolve names into some
information:

```
% blaeu-resolve www.afnic.fr
[2001:41d0:404:200::2df6] : 5 occurrences 
Test #78818183 done at 2024-09-06T13:31:11Z
```

As you can see, the default DNS type is AAAA (IP address). But you can
ask for others, here, for the mail relay:

```
% blaeu-resolve --type MX proton.me
[10 mail.protonmail.ch. 20 mailsec.protonmail.ch.] : 4 occurrences 
[ERROR: SERVFAIL] : 1 occurrences 
Test #78818319 done at 2024-09-06T13:40:24Z
```

Because of the frequent presence of a lying DNS resolver, this tool is
specially interesting to assess [censorship](https://labs.ripe.net/author/stephane_bortzmeyer/dns-censorship-dns-lies-as-seen-by-ripe-atlas/). Selecting probes by
country is therefore common (but [be careful with some countries](https://labs.ripe.net/author/kistel/ethics-of-ripe-atlas-measurements/)):

```
%  blaeu-resolve --country FR --type A sci-hub.se
[186.2.163.219] : 3 occurrences 
[127.0.0.1] : 2 occurrences 
Test #78818372 done at 2024-09-06T13:44:00Z
```

Here, you can that that two probes use a censoring resolver, returning the
lie `127.0.0.1`.


## blaeu-cert 

This connects to a TLS server and gets the certificate. By default, it
displays the name ("subject", in X.509 parlance):

```
% blaeu-cert fr.wikipedia.org
5 probes reported
[/C=US/ST=California/L=San Francisco/O=Wikimedia Foundation, Inc./CN=*.wikipedia.org] : 5 occurrences 
Test #78818374 done at 2024-09-06T13:44:15Z
```

By default, it uses port 443 but you can change that, here to get the
certificate of a DoT (DNS-over-TLS) public resolver:

```
% blaeu-cert --port 853 dot.bortzmeyer.fr
5 probes reported
[/CN=dot.bortzmeyer.fr] : 5 occurrences 
Test #78818392 done at 2024-09-06T13:46:21Z
```

## blaeu-ntp 

You can test public NTP servers:

```
% blaeu-ntp ntp.nic.fr
5 probes reported
[Version 4, Mode server, Stratum 2] : 5 occurrences 
Test #78818431 done at 2024-09-06T13:50:50Z. Mean time offset: 59.143442 s, mean RTT: 0.080120 s
```

## blaeu-http 

You can do HTTP requests:

```
% blaeu-http fr-par-as2486.anchors.atlas.ripe.net
5 probes reported
Test #78818511 done at 2024-09-06T13:58:12Z
Tests: 5 successful tests (100.0 %), 0 errors (0.0 %), 0 timeouts (0.0 %), average RTT: 157 ms, average header size: 131 bytes, average body size: 103 bytes
```

Target *must* be [an anchor](https://atlas.ripe.net/anchors/) (for
various reasons, not debated here).

You can add a number in the URL, the anchor will return data of this
size:

```
% blaeu-http --path /1000 fr-par-as2486.anchors.atlas.ripe.net
3 probes reported
Test #78818539 done at 2024-09-06T14:00:31Z
Tests: 3 successful tests (100.0 %), 0 errors (0.0 %), 0 timeouts (0.0 %), average RTT: 39 ms, average header size: 131 bytes, average body size: 1106 bytes
```

(The extra bytes are because of the JSON encoding of the answer.)

A common workaround to the anchor-only limit is to use `blaeu-cert` to test HTTP reachability
since the vast majority of HTTP servers are HTTPS.

## For all commands

Remember you can get the complete list of options with `-h`.


