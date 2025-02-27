import datetime

class UpdateMixin:

    def update_version(self, increment):

        output = []

        current_version = self.get_version()

        version_values = [int(number) for number in current_version.split('.')]
        increment_value = [int(number) for number in increment.split('.')]

        for i,_ in enumerate(version_values):
            output.append(str(version_values[i] + increment_value[i]))
        
        return '.'.join(output)

    def update_logs(self, event_list):


        version_query = """
        INSERT INTO model_log (
            version,
            user, 
            date,
            event) 
            VALUES 
            (?,?,?,?)
            """
        
        for event in event_list:
            version_value_string = (self.version,
                                    self.user,
                                    datetime.datetime.now(),
                                    event
                                    )

            self.cursor.execute(version_query, version_value_string)




    def update_model_info(self):
        """
        Adds a new model version
        
        Parameters:
        None

        Returns:
        None
        """     

        version_query = """
        INSERT INTO model_info (
            version,
            user, 
            date, 
            nodes, 
            bars, 
            sections, 
            materials, 
            loads, 
            supports, 
            errors, 
            warnings, 
            run_time) 
            VALUES 
            (?,?,?,?,?,?,?,?,?,?,?,?)
            """

        version_value_string = (self.version,
                                self.user,
                                datetime.datetime.now(),
                                self.get_node_count(),
                                self.get_bar_count(),
                                self.get_section_count(),
                                self.get_material_count(),
                                self.get_pointload_count(),
                                self.get_support_count(),
                                None, #TODO
                                None, #TODO
                                self.runtime
                                )

        self.cursor.execute(version_query, version_value_string)

    
    