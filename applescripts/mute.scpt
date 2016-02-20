on run(arguments)
  set e to item 1 of arguments
  tell app "itunes"
    set v to the sound volume
  end tell
  tell app "itunes" to set the sound volume to 0
  set done to 0
  repeat while done = 0
    tell app "itunes"
      set p to player position
    end tell
    if p >= e
      set done to 1
    end if
  end repeat 
  tell app "itunes" to set the sound volume to v
end run