Hard


spawn_pattern = random.choice(["single-single-double", "double-single-single", "single-double-single"])
                if spawn_pattern == "single-single-double":
                    # First single obstacle
                    choice = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))

                    # Second single obstacle
                    choice = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                    obstacles[-1].rect.x += random.randint(600, 800)  # Adjust x-axis for spacing

                    # Double obstacles
                    choice1 = random.randint(0, 2)
                    choice2 = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                    obstacles[-1].rect.x += random.randint(1000, 1200)  # Adjust x-axis for spacing
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                    obstacles[-1].rect.x += random.randint(1400, 1600)  # Adjust x-axis for spacing

                elif spawn_pattern == "double-single-single":
                    # Double obstacles
                    choice1 = random.randint(0, 2)
                    choice2 = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                    obstacles[-1].rect.x += random.randint(600, 800)  # Adjust x-axis for spacing
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                    obstacles[-1].rect.x += random.randint(1000, 1200)  # Adjust x-axis for spacing

                    # First single obstacle
                    choice = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                    obstacles[-1].rect.x += random.randint(1400, 1600)  # Adjust x-axis for spacing

                    # Second single obstacle
                    choice = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                    obstacles[-1].rect.x += random.randint(1800, 2000)  # Adjust x-axis for spacing

                elif spawn_pattern == "single-double-single":
                    # First single obstacle
                    choice = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))

                    # Double obstacles
                    choice1 = random.randint(0, 2)
                    choice2 = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice1]([small_cactus, large_cactus, bird_img][choice1]))
                    obstacles[-1].rect.x += random.randint(600, 800)  # Adjust x-axis for spacing
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice2]([small_cactus, large_cactus, bird_img][choice2]))
                    obstacles[-1].rect.x += random.randint(1000, 1200)  # Adjust x-axis for spacing

                    # Second single obstacle
                    choice = random.randint(0, 2)
                    obstacles.append([SmallCactus, LargeCactus, BirdIndex][choice]([small_cactus, large_cactus, bird_img][choice]))
                    obstacles[-1].rect.x += random.randint(1400, 1600)  # Adjust x-axis for spacing


# Triple Obstacle
                else:
                    obstacles.append(BirdIndex(bird_img))
                    obstacles[-1].rect.x += random.randint(50, 100)  # Adjust x-axis for spacing
                    obstacles.append(SmallCactus(small_cactus))
                    obstacles[-1].rect.x += random.randint(500, 600)  # Adjust x-axis for spacing
                    obstacles.append(BirdIndex(bird_img))
                    obstacles[-1].rect.x += random.randint(1000, 1200)  # Adjust x-axis for spacing