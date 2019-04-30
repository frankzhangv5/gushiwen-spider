function main(splash, args)
    assert(splash:go(splash.args.url))
    local elems = splash:select_all('div.left div.sons div.contyishang div a:last-child')
 
    for i,elem in ipairs(elems) do
        if (elem:text() == '展开阅读全文 ∨')
        then
            local str = elem:getAttribute('href')
            local func = string.sub(str, 12, -1)
            -- print(func)
            assert(splash:runjs(string.format('eval(%s)', func)))
        else
            print('no match items' )
        end
    end
    splash:wait(0.25)
    return splash:html()
end