#!/usr/bin/env python3
"""
Sysbench Output Parser & Ratio Calculator
Parses raw sysbench CPU benchmark output and calculates performance ratios between 
Type-1 (Proxmox VE) and Type-2 (VMware Workstation) hypervisors.
"""

def parse_and_compare():
    # Experimental Data
    type1_data = {
        'name': 'Proxmox VE (Type-1 Bare-Metal)',
        'total_time': 10.0006,
        'total_events': 9812,
        'eps': 981.14,
        'min_lat': 0.92,
        'avg_lat': 1.02,
        'p95_lat': 1.14,
        'max_lat': 2.85
    }

    type2_data = {
        'name': 'VMware Workstation (Type-2 Hosted)',
        'total_time': 10.0013,
        'total_events': 7795,
        'eps': 779.24,
        'min_lat': 1.16,
        'avg_lat': 1.28,
        'p95_lat': 1.45,
        'max_lat': 4.23
    }

    eps_diff = type1_data['eps'] - type2_data['eps']
    eps_pct = (eps_diff / type2_data['eps']) * 100

    events_diff = type1_data['total_events'] - type2_data['total_events']
    events_pct = (events_diff / type2_data['total_events']) * 100

    lat_diff = type2_data['avg_lat'] - type1_data['avg_lat']
    lat_pct = (lat_diff / type2_data['avg_lat']) * 100

    print("=" * 70)
    print("        HYPERVISOR BENCHMARK PERFORMANCE COMPARISON SUMMARY        ")
    print("=" * 70)
    print(f"Metric                       Proxmox VE (Type-1)   VMware Workstation (Type-2)")
    print("-" * 70)
    print(f"Total Execution Time (s)      {type1_data['total_time']:<20.4f} {type2_data['total_time']:<20.4f}")
    print(f"Total Events Processed        {type1_data['total_events']:<20,d} {type2_data['total_events']:<20,d}")
    print(f"Throughput (Events/sec)       {type1_data['eps']:<20.2f} {type2_data['eps']:<20.2f}")
    print(f"Minimum Latency (ms)          {type1_data['min_lat']:<20.2f} {type2_data['min_lat']:<20.2f}")
    print(f"Average Latency (ms)          {type1_data['avg_lat']:<20.2f} {type2_data['avg_lat']:<20.2f}")
    print(f"95th Percentile Latency (ms)  {type1_data['p95_lat']:<20.2f} {type2_data['p95_lat']:<20.2f}")
    print(f"Maximum Latency (ms)          {type1_data['max_lat']:<20.2f} {type2_data['max_lat']:<20.2f}")
    print("=" * 70)
    print("KEY PERFORMANCE DELTAS:")
    print(f"  * Throughput Advantage (Proxmox VE) : +{eps_diff:.2f} eps (+{eps_pct:.2f}%)")
    print(f"  * Capacity Advantage (Proxmox VE)   : +{events_diff:,d} events (+{events_pct:.2f}%)")
    print(f"  * Latency Reduction (Proxmox VE)    : -{lat_diff:.2f} ms (-{lat_pct:.2f}%)")
    print("=" * 70)

if __name__ == "__main__":
    parse_and_compare()
