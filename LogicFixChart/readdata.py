from visualize import ReadCSV, Visualize

def main():
    file_path = "./Current_Employee_Names__Salaries__and_Position_Titles_-_Full-time.csv" 
    data_reader = ReadCSV(file_path)
    user_input = "display the top job titles based on the number of employees by bar chart."
    Visualize(data_reader.df, user_input)
    
if __name__ == '__main__':
    main()