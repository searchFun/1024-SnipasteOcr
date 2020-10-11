// String -> Date
export function str2Date (dateString, fmt) {
  let defaultValue = new Date()
  let matchs = {
    year: {
      reg: 'y+',
      value: defaultValue.getFullYear()
    },
    month: {
      reg: 'M+',
      value: defaultValue.getMonth() + 1
    },
    day: {
      reg: 'd+',
      value: defaultValue.getDate()
    },
    hour: {
      reg: 'H+',
      value: defaultValue.getHours()
    },
    minutes: {
      reg: 'm+',
      value: defaultValue.getMinutes()
    },
    seconds: {
      reg: 's+',
      value: defaultValue.getSeconds()
    }
  }
  for (let key in matchs) {
    if (new RegExp(`(${matchs[key]['reg']})`).test(fmt)) {
      let matchStr = RegExp.$1
      let positon = fmt.indexOf(matchStr)
      let length = matchStr.length
      matchs[key]['value'] = parseInt(dateString.slice(positon, positon + length))
    }
  }
  return new Date(
    matchs.year.value,
    matchs.month.value + 1,
    matchs.day.value,
    matchs.hour.value,
    matchs.minutes.value,
    matchs.seconds.value
  )
}

// Date -> String
export function date2Str (date, fmt) {
  let mactchs = {
    'y+': date.getFullYear(),
    'M+': date.getMonth() + 1,
    'd+': date.getDate(),
    'H+': date.getHours(),
    'm+': date.getMinutes(),
    's+': date.getSeconds()
  }
  for (let match in mactchs) {
    if (new RegExp(`(${match})`).test(fmt)) {
      switch (match) {
        case 'y+':
          {
            let str = mactchs[match] + ''
            fmt = fmt.replace(RegExp.$1, str.substr(4 - RegExp.$1.length))
          }
          break
        default:
          {
            let str = mactchs[match] + ''
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? str : padLeftZero(str))
          }
          break
      }
    }
  }
  return fmt
}

// 左填充0
function padLeftZero (str) {
  return ('00' + str).substr(str.length)
}

export function firstDateOfWeek (date) {
  let tDate = new Date(date.getTime())
  return dateAdd(tDate, -1 * tDate.getDay())
}

export function dateAdd (date, days) {
  let tDate = new Date(date.getTime())
  tDate.setDate(tDate.getDate() + days)
  return tDate
}

export function dateCompare (date1, date2) {
  if (date1.getTime() < date2.getTime()) {
    return -1
  } else if (date1.getTime() > date2.getTime()) {
    return 1
  } else {
    return 0
  }
}
