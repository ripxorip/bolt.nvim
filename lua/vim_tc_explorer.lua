local function charblob_bytes_iter(lines)
  local init_s = {
    next_line_idx = 1,
    next_byte_idx = 1,
    lines = lines,
  }
  local function next(s, _)
    if lines[s.next_line_idx] == nil then
      return nil
    end
    if s.next_byte_idx > #(lines[s.next_line_idx]) then
      s.next_line_idx = s.next_line_idx + 1
      s.next_byte_idx = 1
      return ('\n'):byte()
    end
    local ret = lines[s.next_line_idx]:byte(s.next_byte_idx)
    if ret == ('\n'):byte() then
      ret = 0  -- See :h NL-used-for-NUL.
    end
    s.next_byte_idx = s.next_byte_idx + 1
    return ret
  end
  return next, init_s, nil
end

local function charblob_encode(lines, textwidth, indent)
  local ret = {
    'const char blob[] = {',
    indent,
  }
  for byte in charblob_bytes_iter(lines) do
    --                .- space + number (width 3) + comma
    if #(ret[#ret]) + 5 > textwidth then
      ret[#ret + 1] = indent
    else
      ret[#ret] = ret[#ret] .. ' '
    end
    ret[#ret] = ret[#ret] .. (('%3u,'):format(byte))
  end
  ret[#ret + 1] = '};'
  return ret
end

return {
  bytes_iter = charblob_bytes_iter,
  migic = charblob_encode,
}

