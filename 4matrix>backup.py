def snake_led_number(x, y):
        color = (0, 0, 255)

        led_number: int = x * MATRIX_HEIGHT + y
        if (math.floor(led_number / MATRIX_HEIGHT) % 2) == 1:
          pixel =  (x + 1) * MATRIX_HEIGHT - y - 1
        else:
          pixel = led_number
        delimeter = (y // 8) 

            
        if delimeter % 2 == 1:
          if (y % 2 == 0):
            pixel = delimeter * 256 + (((MATRIX_WIDTH - x)  - delimeter - 1 ) * MATRIX_HEIGHT) + y
            color = (0, 255, 0) #  green

          else:
          #     pixel = delimeter*256 - pixel  + x * MATRIX_WIDTH 
            pixel = delimeter * 256 + (MATRIX_WIDTH - x + 1) * MATRIX_HEIGHT + y
            color = (255, 0 , 0) #  red
        print(x, y, delimeter, " : ",pixel)
        

        return abs(pixel), color