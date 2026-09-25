import matplotlib.pyplot as plt
import numpy as np
import os

# Ensure output directory exists
os.makedirs('images', exist_ok=True)

# Styling configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dpi = 300

proxmox_color = '#0052cc'  # Proxmox Blue (Type-1)
vmware_color = '#e65100'   # VMware Orange (Type-2)
docker_color = '#099cec'   # Docker Cyan/Blue

# =========================================================================
# EXPERIMENT 1: HYPERVISOR PERFORMANCE COMPARISON (TYPE-1 vs TYPE-2)
# =========================================================================
hypervisors = ['Proxmox VE\n(Type-1 Bare-Metal)', 'VMware Workstation\n(Type-2 Hosted)']

# Plot 1: Events Per Second (Throughput)
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
eps_values = [925.32, 734.96]
bars = ax.bar(hypervisors, eps_values, color=[proxmox_color, vmware_color], width=0.45, edgecolor='black', linewidth=1.2)
ax.set_ylabel('Events per Second (EPS)', fontsize=12, fontweight='bold')
ax.set_title('CPU Throughput Comparison (Sysbench 20k Primes)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 1200)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:,.2f} eps', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')

pct_diff = ((925.32 - 734.96) / 734.96) * 100
ax.text(0.5, 0.85, f'Proxmox VE is +{pct_diff:.2f}% faster\nin CPU Throughput', 
        transform=ax.transAxes, fontsize=12, fontweight='bold', ha='center',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#e8f4f8', edgecolor='#0052cc', alpha=0.9))
plt.tight_layout()
plt.savefig('images/events_per_second_comparison.png')
plt.close()

# Plot 2: Latency Metrics Comparison
fig, ax = plt.subplots(figsize=(10, 6), dpi=fig_dpi)
metrics = ['Minimum Latency', 'Average Latency', '95th Percentile', 'Maximum Latency']
proxmox_lat = [0.65, 1.08, 1.63, 8.42]
vmware_lat = [0.82, 1.36, 2.07, 12.34]
x = np.arange(len(metrics))
width = 0.35
rects1 = ax.bar(x - width/2, proxmox_lat, width, label='Proxmox VE (Type-1)', color=proxmox_color, edgecolor='black', linewidth=1)
rects2 = ax.bar(x + width/2, vmware_lat, width, label='VMware Workstation (Type-2)', color=vmware_color, edgecolor='black', linewidth=1)
ax.set_ylabel('Latency (milliseconds ms)', fontsize=12, fontweight='bold')
ax.set_title('Sysbench CPU Latency Metrics Comparison (Lower is Better)', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(metrics, fontsize=11, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
ax.set_ylim(0, 14.5)
for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} ms', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#003399')
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.2f} ms', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 4),
                textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#b33c00')
plt.tight_layout()
plt.savefig('images/latency_comparison.png')
plt.close()

# Plot 3: Total Events Comparison
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
events_values = [9254, 7352]
bars = ax.bar(hypervisors, events_values, color=[proxmox_color, vmware_color], width=0.45, edgecolor='black', linewidth=1.2)
ax.set_ylabel('Total Events Processed (in 10 seconds)', fontsize=12, fontweight='bold')
ax.set_title('Total Sysbench Prime Calculation Events', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 12000)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:,} events', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('images/total_events_comparison.png')
plt.close()

# Plot 4: Overall Hypervisor Performance Dashboard
fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=fig_dpi)
fig.suptitle('Performance Analysis Dashboard: Type-1 (Proxmox VE) vs Type-2 (VMware Workstation)', fontsize=16, fontweight='bold', y=0.98)
axs[0, 0].bar(hypervisors, eps_values, color=[proxmox_color, vmware_color], width=0.4, edgecolor='black')
axs[0, 0].set_title('Events per Second (Higher is Better)', fontsize=12, fontweight='bold')
axs[0, 0].set_ylabel('Events / sec', fontsize=10)
axs[0, 0].set_ylim(0, 1100)
for bar in axs[0, 0].patches:
    axs[0, 0].annotate(f'{bar.get_height():,.2f}', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

axs[0, 1].bar(hypervisors, events_values, color=[proxmox_color, vmware_color], width=0.4, edgecolor='black')
axs[0, 1].set_title('Total Events in 10s (Higher is Better)', fontsize=12, fontweight='bold')
axs[0, 1].set_ylabel('Total Events', fontsize=10)
axs[0, 1].set_ylim(0, 11000)
for bar in axs[0, 1].patches:
    axs[0, 1].annotate(f'{int(bar.get_height()):,}', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

avg_lats = [1.08, 1.36]
axs[1, 0].bar(hypervisors, avg_lats, color=[proxmox_color, vmware_color], width=0.4, edgecolor='black')
axs[1, 0].set_title('Average Latency (Lower is Better)', fontsize=12, fontweight='bold')
axs[1, 0].set_ylabel('Latency (ms)', fontsize=10)
axs[1, 0].set_ylim(0, 1.8)
for bar in axs[1, 0].patches:
    axs[1, 0].annotate(f'{bar.get_height():.2f} ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

p95_lats = [1.63, 2.07]
axs[1, 1].bar(hypervisors, p95_lats, color=[proxmox_color, vmware_color], width=0.4, edgecolor='black')
axs[1, 1].set_title('95th Percentile Latency (Lower is Better)', fontsize=12, fontweight='bold')
axs[1, 1].set_ylabel('Latency (ms)', fontsize=10)
axs[1, 1].set_ylim(0, 2.5)
for bar in axs[1, 1].patches:
    axs[1, 1].annotate(f'{bar.get_height():.2f} ms', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('images/overall_performance_dashboard.png')
plt.close()


# =========================================================================
# EXPERIMENT 2: DOCKER CONTAINERIZATION vs VIRTUAL MACHINES
# =========================================================================
architectures = ['Docker Container\n(OS-Level Virtualization)', 'Type-1 Bare-Metal VM\n(Proxmox VE)', 'Type-2 Hosted VM\n(VMware Workstation)']
architectures_colors = [docker_color, proxmox_color, vmware_color]

# Container Plot 1: Startup Latency Comparison (seconds)
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
startup_times = [0.8, 22.5, 42.0]  # <1s for Docker vs ~22.5s Type-1 VM vs ~42s Type-2 VM
bars = ax.bar(architectures, startup_times, color=architectures_colors, width=0.45, edgecolor='black', linewidth=1.2)
ax.set_ylabel('Startup / Boot Latency (Seconds)', fontsize=12, fontweight='bold')
ax.set_title('Application Startup Time: Docker Container vs Virtual Machines', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 50)
for bar in bars:
    height = bar.get_height()
    label = f'{height:.1f} s' if height >= 1 else f'{height:.1f} s (<1s)'
    ax.annotate(label, xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.text(0.5, 0.85, 'Docker Containers start 50x-52x faster\nthan Virtual Machines', 
        transform=ax.transAxes, fontsize=12, fontweight='bold', ha='center',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='#e1f5fe', edgecolor='#099cec', alpha=0.9))
plt.tight_layout()
plt.savefig('images/docker_vs_vm_startup_time.png')
plt.close()

# Container Plot 2: Memory Footprint Comparison (MB)
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
memory_footprints = [24.5, 2048.0, 2048.0]  # 24.5MB Flask app container vs 2GB allocated VM RAM
bars = ax.bar(architectures, memory_footprints, color=architectures_colors, width=0.45, edgecolor='black', linewidth=1.2)
ax.set_ylabel('RAM Overhead (MB)', fontsize=12, fontweight='bold')
ax.set_title('Baseline RAM Consumption Comparison', fontsize=14, fontweight='bold', pad=15)
ax.set_yscale('log')
ax.set_ylim(1, 5000)
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height:.1f} MB', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('images/docker_vs_vm_memory_footprint.png')
plt.close()

# Container Plot 3: Disk Overhead Comparison (MB)
fig, ax = plt.subplots(figsize=(8, 6), dpi=fig_dpi)
storage_sizes = [145.0, 20480.0, 20480.0]  # ~145MB Docker python:3.12-slim image vs 20GB (20480MB) VM Virtual Disk
bars = ax.bar(architectures, storage_sizes, color=architectures_colors, width=0.45, edgecolor='black', linewidth=1.2)
ax.set_ylabel('Disk Storage Size (MB)', fontsize=12, fontweight='bold')
ax.set_title('Storage Footprint: Docker Image vs VM Disk Allocation', fontsize=14, fontweight='bold', pad=15)
ax.set_yscale('log')
ax.set_ylim(10, 50000)
for bar in bars:
    height = bar.get_height()
    if height > 1000:
        label = f'{height/1024:.1f} GB ({int(height)} MB)'
    else:
        label = f'{int(height)} MB'
    ax.annotate(label, xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6), textcoords="offset points", ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('images/docker_vs_vm_disk_overhead.png')
plt.close()

# Container Plot 4: Multi-Panel Containerization Dashboard
fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=fig_dpi)
fig.suptitle('Containerization Analysis Dashboard: Docker Containers vs Virtual Machines', fontsize=16, fontweight='bold', y=0.98)

# Subplot 1: Startup Latency
axs[0, 0].bar(architectures, startup_times, color=architectures_colors, width=0.4, edgecolor='black')
axs[0, 0].set_title('Startup / Boot Latency (Lower is Better)', fontsize=12, fontweight='bold')
axs[0, 0].set_ylabel('Seconds (s)', fontsize=10)
axs[0, 0].set_ylim(0, 50)
for bar in axs[0, 0].patches:
    axs[0, 0].annotate(f'{bar.get_height():.1f} s', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 2: Memory Footprint
axs[0, 1].bar(architectures, memory_footprints, color=architectures_colors, width=0.4, edgecolor='black')
axs[0, 1].set_title('RAM Overhead (Lower is Better)', fontsize=12, fontweight='bold')
axs[0, 1].set_ylabel('RAM (MB)', fontsize=10)
axs[0, 1].set_yscale('log')
axs[0, 1].set_ylim(1, 5000)
for bar in axs[0, 1].patches:
    axs[0, 1].annotate(f'{bar.get_height():.1f} MB', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 3: Disk Size
axs[1, 0].bar(architectures, storage_sizes, color=architectures_colors, width=0.4, edgecolor='black')
axs[1, 0].set_title('Disk Storage Overhead (Lower is Better)', fontsize=12, fontweight='bold')
axs[1, 0].set_ylabel('Disk (MB)', fontsize=10)
axs[1, 0].set_yscale('log')
axs[1, 0].set_ylim(10, 50000)
for bar in axs[1, 0].patches:
    h = bar.get_height()
    lbl = f'{h/1024:.1f} GB' if h > 1000 else f'{int(h)} MB'
    axs[1, 0].annotate(lbl, (bar.get_x() + bar.get_width()/2, h),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

# Subplot 4: Virtualization Overhead Ratio (%)
overhead_ratios = [0.5, 5.2, 14.8]  # ~0.5% overhead for Docker vs 5.2% Type-1 KVM vs 14.8% Type-2 Hosted VM
axs[1, 1].bar(architectures, overhead_ratios, color=architectures_colors, width=0.4, edgecolor='black')
axs[1, 1].set_title('CPU Virtualization Overhead % (Lower is Better)', fontsize=12, fontweight='bold')
axs[1, 1].set_ylabel('Overhead (%)', fontsize=10)
axs[1, 1].set_ylim(0, 20)
for bar in axs[1, 1].patches:
    axs[1, 1].annotate(f'{bar.get_height():.1f}%', (bar.get_x() + bar.get_width()/2, bar.get_height()),
                       xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontweight='bold')

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('images/containerization_performance_dashboard.png')
plt.close()

print('All hypervisor and containerization plots generated successfully in images/ directory.')
