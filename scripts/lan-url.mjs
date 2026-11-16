/**
 * 打印手机可访问的局域网地址（预览服务已监听 0.0.0.0，无需额外配置）
 * 用法：npm run lan [端口，默认 4173]
 */
import { networkInterfaces } from 'node:os'

const port = process.argv[2] ?? '4173'

// 排除虚拟网卡（Hyper-V / VMware / VirtualBox / WSL / 回环），只留真实局域网
const VIRTUAL = /vethernet|hyper-v|vmware|virtualbox|loopback|wsl|tailscale|zerotier/i

const ips = Object.entries(networkInterfaces())
  .filter(([name]) => !VIRTUAL.test(name))
  .flatMap(([, infos]) => infos ?? [])
  .filter((info) => info.family === 'IPv4' && !info.internal)
  .map((info) => info.address)
  .filter((address) => !address.startsWith('169.254.'))

if (!ips.length) {
  console.log('未找到局域网 IPv4 地址，请确认电脑已连接 WiFi 或网线')
  process.exit(0)
}

console.log('')
console.log('手机（需与电脑同一 WiFi）可访问：')
for (const address of ips) {
  console.log(`  http://${address}:${port}/guide/motion`)
}
console.log('')
console.log('提示：localhost 在手机上指向手机自己，必须用上面的 IP。')
