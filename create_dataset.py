import pandas as pd
import numpy as np

from tqdm import tqdm

from collections import Counter
pd.options.mode.chained_assignment = None
PATH = "datasets/train_dataset_VK/"
test_filename = "test_1M_40.csv"
attr_filename = "attr.csv"
rich_test_filename = "rich_v3_test_1M_40.csv"

src_attr_df = pd.read_csv(PATH + attr_filename)
test_df = pd.read_csv(PATH + test_filename)

ego_nums = test_df["ego_id"].unique()



# Общая обработка данных 

# Вводим новый критерий сущесвтует ли t, это доп параметр к t 
test_df["is_t_exist"] = 1
test_df.loc[test_df["t"].isna(), ["is_t_exist"]] = 0
test_df["t"] = test_df["t"].fillna(0)

# OHE для пола потому что там есть неопределнные значения
attr_df = pd.get_dummies(src_attr_df, prefix="sex", columns=["sex"])
# Возраст если не указан то берем средний
attr_df["age"][(attr_df["age"] == -1)|(attr_df["age"] >= 80)] = int(attr_df["age"].mean())

egos = test_df["ego_id"].unique()
union_df = pd.DataFrame()

for ego_id in tqdm(egos[:130]):
    print(f"ego_id: {ego_id}")
    ego_df = test_df[test_df["ego_id"] == ego_id]
    ego_attr_df = attr_df[attr_df["ego_id"] == ego_id]
    
    ego_df["ego_age"] = int(ego_attr_df["age"].mean())
    
    
    # Базовый расчет средней интенсивности friendship
    ego_df["friendship"] = ego_df.apply(lambda x: ego_df[(ego_df["u"] == x["u"])|(ego_df["v"] == x["u"])|(ego_df["u"] == x["v"])|(ego_df["v"] == x["v"])]["x1"].mean(), axis=1)
    ego_df["friendship_x2"] = ego_df.apply(lambda x: ego_df[(ego_df["u"] == x["u"])|(ego_df["v"] == x["u"])|(ego_df["u"] == x["v"])|(ego_df["v"] == x["v"])]["x2"].mean(), axis=1)
    ego_df["friendship_x3"] = ego_df.apply(lambda x: ego_df[(ego_df["u"] == x["u"])|(ego_df["v"] == x["u"])|(ego_df["u"] == x["v"])|(ego_df["v"] == x["v"])]["x3"].mean(), axis=1)
    ego_df["friendship_x3_cnt"] = ego_df.apply(lambda x: ego_df[(ego_df["u"] == x["u"])|(ego_df["v"] == x["u"])|(ego_df["u"] == x["v"])|(ego_df["v"] == x["v"])]["x3"].sum(), axis=1)
    
    
    # Меняем значение городов/школ/универов на частоту их встречания внутри его-графа
    city_counter = Counter(ego_attr_df["city_id"].values)
    city_counter[-1] = city_counter.most_common(1)[0][1]
    ego_attr_df["city_freq"] = ego_attr_df.apply(lambda x: city_counter[x["city_id"]], axis=1)
        
    univer_counter = Counter(ego_attr_df["university"].values)
    univer_counter[-1] = univer_counter.most_common(1)[0][1]
    ego_attr_df["university_freq"] = ego_attr_df.apply(lambda x: univer_counter[x["university"]], axis=1)
    
    school_counter = Counter(ego_attr_df["school"].values)
    school_counter[-1] = school_counter.most_common(1)[0][1]
    ego_attr_df["school_freq"] = ego_attr_df.apply(lambda x: school_counter[x["school"]], axis=1)
    
    # Объединяем атрибуты с вершинами U V
    union_ego = ego_df.merge(ego_attr_df[["ego_id", "u", "age", "sex_1", "sex_2", "city_freq", "university_freq", "school_freq", "city_id", "university", "school"]], left_on=["ego_id", "u"], right_on=["ego_id", "u"])
    
    union_ego = union_ego.merge(ego_attr_df[["ego_id", "u", "age", "sex_1", "sex_2", "city_freq", "university_freq", "school_freq", "city_id", "university", "school"]], left_on=["ego_id", "v"], right_on=["ego_id", "u"])
    union_df = pd.concat([union_df, union_ego], axis=0)

    # union_df["eqaul_sex"] = union_df.apply(lambda x: 1 if (x["sex_2_x"] == x["sex_2_y"]) or (x["sex_1_x"] == x["sex_1_y"]) else 0, axis=1)
    # union_df["eqaul_school"] = union_df.apply(lambda x: 1 if x["school_x"] != -1 and (x["school_x"] == x["school_y"]) else 0, axis=1)
    # union_df["eqaul_university"] = union_df.apply(lambda x: 1 if x["university_x"] != -1 and  (x["university_x"] == x["university_y"]) else 0, axis=1)
    # union_df["eqaul_city"] = union_df.apply(lambda x: 1 if (x["city_id_x"] == x["city_id_y"]) else 0, axis=1)
    # union_df["delta_age"] = abs(union_df["age_x"] - union_df["age_y"])
    

    # union_df["friend_age_u"] = union_df.apply(lambda x: (union_df[(union_df["u_x"] == x["u_x"])]["age_x"].mean() + union_df[(union_df["v"] == x["u_x"])]["age_x"].mean())//2, axis=1)
    # union_df["friend_age_v"] = union_df.apply(lambda x: (union_df[(union_df["u_x"] == x["u_x"])]["age_y"].mean() + union_df[(union_df["v"] == x["u_x"])]["age_y"].mean())//2, axis=1)
    # union_df["delta_friend_age"] = abs(union_df["friend_age_u"] - union_df["friend_age_v"])
    
    union_df["time_by_ages"] = union_df["t"]/union_df["age_x"]
    union_df["time_by_friendship"] = union_df["t"]/union_df["friendship"]
    union_df["time_by_friendship_x2"] = union_df["t"]/union_df["friendship_x2"]
    union_df["time_by_friendship_x3"] = union_df["t"]/union_df["friendship_x3"]

    # union_df["time_by_ages_dot"] = union_df["t"]*union_df["age_x"]
    # union_df["time_by_friendship_dot"] = union_df["t"]*union_df["friendship"]
    # union_df["time_by_friendship_x2_dot"] = union_df["t"]*union_df["friendship_x2"]
    # union_df["time_by_friendship_x3_dot"] = union_df["t"]*union_df["friendship_x3"]


    
union_df = union_df[['ego_id', 'u_x', 'v', 't', 'x1', 'x2', 'x3', 'is_t_exist',  'age_x', 'sex_1_x', 'sex_2_x', 'city_freq_x', 'university_freq_x', 'school_freq_x', 'age_y', 'sex_1_y', 'sex_2_y', 'city_freq_y', 'university_freq_y', 
                     'school_freq_y', "ego_age",  
                    'friendship', "friendship_x2", "friendship_x3", "friendship_x3_cnt", 
                     # "eqaul_sex", "eqaul_school", "eqaul_university", "eqaul_city", "delta_age", 
                     # "friend_age_u", "friend_age_v", "delta_friend_age",
                     "time_by_ages", "time_by_friendship", "time_by_friendship_x2", "time_by_friendship_x3", 
                     
                    ]]
union_df = union_df.rename(columns={"u_x": "u"})
union_df["friendship"] = union_df["friendship"].fillna(0)


union_df.to_csv(PATH + rich_test_filename, index=False)
