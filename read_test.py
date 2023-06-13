# filename = "train.csv"
PATH = "datasets/train_dataset_VK/"
filename = "test.csv"


prefix = filename.split(".")[0]

with open(PATH + filename, "r") as file:
	head = file.readline()
	count_file = 0
	print(f"{prefix}_{count_file}.csv")
	sub_file = open(PATH + f"{prefix}_{count_file}.csv", 'w')
	sub_file.write(head)

	count_row = 0
	current_ego_id = ""
	for row in file:
		count_row += 1
		if count_row > 1_000_000:
			arr_row = row.split(",")
			if current_ego_id == "":
				current_ego_id = arr_row[0]
			elif current_ego_id != arr_row[0]:
				count_file += 1
				count_row = 0
				current_ego_id = ""
				sub_file.close()
				print(f"{prefix}_{count_file}.csv")
				sub_file = open(PATH + f"{prefix}_1M_{count_file}.csv", 'w')
				sub_file.write(head)
		sub_file.write(row)
sub_file.close()
