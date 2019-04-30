function main(splash, args)
    assert(splash:go(splash.args.url))
 
    local result = {}
    local poem_elem = splash:select('div.main3 div.left div.sons')
    local poet_elem = splash:select('div.sonspic')
    local btns = splash:select('div.yizhu'):querySelectorAll('img')

    if (poem_elem ~= nil)
    then
        result['poem'] = poem_elem.innerHTML
    end

    if (poet_elem ~= nil)
    then
        result['poet'] = poet_elem.innerHTML
    end
 
    for i,btn in ipairs(btns) do
        if (btn:getAttribute('alt') == '译文')
        then
            btn:mouse_click()
            local elem = splash:select('div.contson')
            result['translation'] = elem.innerHTML
            btn:mouse_click()
        elseif(btn:getAttribute('alt') == '注释')
        then
            btn:mouse_click()
            local elem = splash:select('div.contson')
            result['annotation'] = elem.innerHTML
            btn:mouse_click()
        elseif(btn:getAttribute('alt') == '赏析')
        then
            btn:mouse_click()
            local elem = splash:select('div.contson')
            result['appreciation'] = elem.innerHTML
            btn:mouse_click()
        else
            print('no match items' )
        end
    end

    return result
end