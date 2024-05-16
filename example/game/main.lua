function love.load()
    width, height = love.graphics.getDimensions()
    square_width = 50
    square_height = square_width
end

function love.draw()
    love.graphics.rectangle('fill', width/2 - square_width/2, height/2 - square_height/2, square_width, square_height)
end