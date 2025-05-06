import salt.client

def detect():
    """
    Detects any unexpected changes (infrastructure drift) using a test=True highstate.
    """
    local = salt.client.LocalClient()
    results = local.cmd('*', 'state.apply', [], {'test': True})

    drifted = {}

    for minion, states in results.items():
        if isinstance(states, dict):
            changed = {
                k: v for k, v in states.items()
                if isinstance(v, dict) and v.get('result') is None and v.get('changes')
            }
            if changed:
                drifted[minion] = changed

    if not drifted:
        return "✅ No drift detected on any minions."
    else:
        return drifted
