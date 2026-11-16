/** 极简高亮：只认注释、标签、属性名、字符串、插值，够用且不引入额外依赖 */

const ESCAPE: Record<string, string> = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
}

function escapeHtml(str: string): string {
  return str.replace(/[&<>]/g, (c) => ESCAPE[c])
}

/**
 * 注意：先转义再匹配，所以标签在文本里是 &lt;tag&gt; 的形式，
 * 引号故意不转义，字符串才匹配得到。
 * 分组：1 注释 / 2 开标签 / 3 标签名 / 4 闭标签 / 5 空格 / 6 属性名 / 7 等号 / 8 字符串 / 9 插值
 */
const TOKEN =
  /(&lt;!--[\s\S]*?--&gt;)|(&lt;\/?)([A-Za-z][\w.:-]*)|(&gt;|\/&gt;)|(\s)([@:vA-Za-z][\w:.-]*)(=)|("[^"]*"|'[^']*')|(\{\{[\s\S]*?\}\})/g

export function highlight(code: string): string {
  const src = escapeHtml(code)
  let out = ''
  let last = 0
  let m: RegExpExecArray | null

  TOKEN.lastIndex = 0
  while ((m = TOKEN.exec(src))) {
    out += src.slice(last, m.index)
    last = m.index + m[0].length

    if (m[1]) {
      out += `<span class="tok-comment">${m[1]}</span>`
    } else if (m[2]) {
      out += `<span class="tok-punc">${m[2]}</span><span class="tok-tag">${m[3]}</span>`
    } else if (m[4]) {
      out += `<span class="tok-punc">${m[4]}</span>`
    } else if (m[5]) {
      out += `${m[5]}<span class="tok-attr">${m[6]}</span><span class="tok-punc">${m[7]}</span>`
    } else if (m[8]) {
      out += `<span class="tok-str">${m[8]}</span>`
    } else if (m[9]) {
      out += `<span class="tok-mustache">${m[9]}</span>`
    }
  }

  out += src.slice(last)
  return out
}
