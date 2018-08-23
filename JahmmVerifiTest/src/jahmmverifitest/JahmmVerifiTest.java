/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package jahmmverifitest;





/**
 *
 * @author Mohammadhia
 */
import java.util.*;
import java.io.*;
 
import be.ac.ulg.montefiore.run.jahmm.*; 
import be.ac.ulg.montefiore.run.jahmm.draw.GenericHmmDrawerDot; 
import be.ac.ulg.montefiore.run.jahmm.learn.BaumWelchLearner; 
import be.ac.ulg.montefiore.run.jahmm.toolbox.KullbackLeiblerDistanceCalculator; 
import be.ac.ulg.montefiore.run.jahmm.toolbox.MarkovGenerator; 
import be.ac.ulg.montefiore.run.jahmm.ViterbiCalculator;
public class JahmmVerifiTest {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException {
        //Building the HMM
        Hmm hmm = new Hmm(4, new OpdfIntegerFactory(10));
        
        hmm.setPi(0, 0.5999999999999996);
        hmm.setPi(1, 0.3999999999999997);
        hmm.setPi(2, 0.0); 
        hmm.setPi(3, 0.0);
        
        hmm.setOpdf(0, new OpdfInteger(new double[] {1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}));
        hmm.setOpdf(1, new OpdfInteger(new double[] {0.0, 0.376, 0.518, 0.106, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}));
        hmm.setOpdf(2, new OpdfInteger(new double[] {0.0, 0.0, 0.0, 0.0, 0.196, 0.798, 0.006, 0.0, 0.0, 0.0}));
        hmm.setOpdf(3, new OpdfInteger(new double[] {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.239, 0.761, 0.0}));
        
        //state 0
        hmm.setAij(0, 0, 0.484);  
        hmm.setAij(0, 1, 0.43);  
        hmm.setAij(0, 2, 0.079);
        hmm.setAij(0, 3, 0.007);
        //state 1
        hmm.setAij(1, 0, 0.12);  
        hmm.setAij(1, 1, 0.462);  
        hmm.setAij(1, 2, 0.269);
        hmm.setAij(1, 3, 0.148);
        //state 2
        hmm.setAij(2, 0, 0.061);  
        hmm.setAij(2, 1, 0.32);  
        hmm.setAij(2, 2, 0.399);
        hmm.setAij(2, 3, 0.219);
        //state 3
        hmm.setAij(3, 0, 0.019);  
        hmm.setAij(3, 1, 0.105);  
        hmm.setAij(3, 2, 0.249);
        hmm.setAij(3, 3, 0.627);

        
        
        //Reading the data
        int totalRow = 94;
        char[][] data = new char[totalRow][];
        File file = new File("src/hmmArrayTestVerifi.txt");
        Scanner scanner = new Scanner(file);
        
        for (int row = 0; scanner.hasNextLine() && row < totalRow; row++) { //Populates array with data
            data[row] = scanner.nextLine().toCharArray();
        }
        
        int totalFormSubmits = 0; //Total number of form submits, which will be used to calculate measure accuracy of model (assuming each form submit is a concluding state)
        int totalCorrectPredictions = 0; //Total correct predictions that form submit is concluding state
        
        ArrayList<ArrayList<String>> userActions = new ArrayList<ArrayList<String>>();
        
        for(int i = 0; i < totalRow; i++){
            Vector sequence = new Vector();
            
            ArrayList<String> currentUsersActions = new ArrayList<String>();
            
            
            for (int j = 0; j < data[i].length; j++) {
                
                if(data[i][j] == '-'){
                    currentUsersActions.add( Character.toString(data[i][j]) ); //Adds action (not from observable actions in HMM) to list
                }
                try{
                    if(Character.isDigit(data[i][j]) && data[i][j-1] == 'F'){ //IF the action was on the Form view
                        int tempValue = data[i][j] - '0';

                        ObservationInteger obs = new ObservationInteger(tempValue);

                        sequence.add(obs);

                        currentUsersActions.add( Character.toString(data[i][j-1]) + data[i][j]); //Adds action (with form submit) to list
                    } else if(Character.isDigit(data[i][j])){
                        int tempValue = data[i][j] - '0';

                        ObservationInteger obs = new ObservationInteger(tempValue);

                        //ObservationInteger obs = new ObservationInteger(Character.getNumericValue(data[i][j]));
                        currentUsersActions.add( Character.toString(data[i][j]) ); //Adds action (not from observable actions in HMM) to list
                        sequence.add(obs);
                    }
                } catch(Exception e) {
                    
                }
                
            }
            
            userActions.add(currentUsersActions);
            System.out.println(sequence);
            
            ArrayList<Integer> formSubmitIndices = new ArrayList<Integer>();
            int formSubmitIndex = -1; //Index is initially -1 (an index of 0 for the first action will be realized with the ++ below)
            for(int k = 0; k < userActions.get(i).size(); k++){
                if(!userActions.get(i).get(k).equals("-")){
                    formSubmitIndex++; //Increases index by 1
                }
                if(userActions.get(i).get(k).equals("F0")){
                    formSubmitIndices.add(new Integer(formSubmitIndex)); //Adds index of each F0
                }
            }
            for(int k = 0; k < formSubmitIndices.size(); k++){
                System.out.println(formSubmitIndices.get(k));
            }
            
            
            
            ViterbiCalculator viterb = new ViterbiCalculator(sequence, hmm);
            for(int k = 0; k < viterb.stateSequence().length; k++){
                System.out.print(viterb.stateSequence()[k] + " ");
            }
            
            totalFormSubmits += formSubmitIndices.size();
            for(int k = 0; k < formSubmitIndices.size(); k++){
                if(viterb.stateSequence()[formSubmitIndices.get(k)] == 3){ //If form submit is predicted to be concluding state
                    totalCorrectPredictions++; //Increase correct prediction count by 1
                }
                else {
                    System.out.println("Actual prediction: " + viterb.stateSequence()[formSubmitIndices.get(k)]);
                }
            }
            
            
//            System.out.println("Total length: " + viterb.stateSequence().length);
//            System.out.println(userActions.get(0));
//            System.out.println("Total length 2: " + userActions.get(0).size());
//            System.out.println("Sample: " + userActions.get(0).get( userActions.get(0).size()-7 ));
//            
//            if(userActions.get(0).get( userActions.get(0).size()-7 ).equals("F0")){
//                System.out.println("CORRECT");
//            }
//            
//            if(viterb.stateSequence()[viterb.stateSequence().length-1] == 0){
//                System.out.println("CORRECT 2");
//            }
//            System.out.println(totalCorrectPredictions);
//            System.out.println(totalFormSubmits);



        }
        
        //System.out.println(userActions.get(0));
        
        double accuracy = ((double) totalCorrectPredictions)/totalFormSubmits;
        System.out.println("Accuracy: " + accuracy);
        
    }
    
}
