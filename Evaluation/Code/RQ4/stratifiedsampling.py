
import pandas as pd
import numpy as np

def stratified_sampling_from_excel(input_file, output_file, sample_size=20):

    df = pd.read_excel(input_file)
    
    # Create a dictionary to store data from each category
    categories = {
        'Fail': df['Fail'].dropna().tolist(),
        'Pass': df['Simple Pass'].dropna().tolist()
    }
    
    total_items = sum(len(items) for items in categories.values())
    
    if total_items < sample_size:
        print(f"Warning: Sample size ({sample_size}) is larger than total items ({total_items})")
        print("Using all available items")
        sample_size = total_items
        use_all_items = True
    else:
        use_all_items = False

    sample_distribution = {}
    for category, items in categories.items():
        if use_all_items:
            sample_distribution[category] = len(items)
        else:
            proportion = len(items) / total_items
            sample_distribution[category] = int(round(proportion * sample_size))
    
    total_sampled = sum(sample_distribution.values())
    if total_sampled != sample_size and not use_all_items:
        largest_category = max(categories.keys(), key=lambda x: len(categories[x]))
        sample_distribution[largest_category] += sample_size - total_sampled
    
    print("Sample distribution:")
    for category, count in sample_distribution.items():
        print(f"  {category}: {count} samples (from {len(categories[category])} total)")
    
    # Perform stratified sampling
    sampled_data = {}
    for category, sample_count in sample_distribution.items():
        population = categories[category]
        
        if sample_count >= len(population):
            # If sample size is larger than or equal to population, take all
            sampled_items = population
            if sample_count > len(population):
                print(f"  Note: {category} has only {len(population)} items, taking all available")
        else:
        
            sampled_items = np.random.choice(population, size=sample_count, replace=False).tolist()
        
        sampled_data[category] = sampled_items
    
    # Create a new DataFrame for the sampled data
    max_length = max(len(items) for items in sampled_data.values())
    
    # Pad shorter lists with empty strings to make all columns equal length
    for category in sampled_data:
        sampled_data[category] += [''] * (max_length - len(sampled_data[category]))
    
    sampled_df = pd.DataFrame(sampled_data)
    
    # Save to new Excel file
    sampled_df.to_excel(output_file, index=False)
    print(f"\nSampled data saved to: {output_file}")
    
    return sampled_df



if __name__ == "__main__":
    for dataset in ['AP-SNG', 'Dave2', 'AP-TWN(R1)', 'AP-TWN(R2)', 'AP-TWN(R3)', 'AP-TWN(R4)', 'AP-DHB', 'Router']:
      
        input_filename = #requires an excel file which has one column for pass assertions and one column for fail assertions
        output_filename = "stratified_sampled_"+input_filename+".xlsx"
        
        sampled_data = stratified_sampling_from_excel(input_filename+'.xlsx', output_filename, sample_size=20)
                
