# Troubleshooting

## Out of tiles

The fabric does not have enough tiles for the requested graph. The certificate
will include the total nodes count; reduce the design or increase fabric size.

## NoC saturation

If NoC links exceed bandwidth, congestion will be listed under `congested_links`.

## Timing not met

Latency constraints will be marked `pass: false` in the certificate.

## Locality constraint impossible

A locality constraint is violated if nodes end up in different islands; re-run
with a larger island or adjust constraints.
