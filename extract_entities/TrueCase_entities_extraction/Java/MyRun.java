import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.ie.util.*;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.semgraph.*;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.*;
import java.util.*;
import edu.stanford.nlp.ling.CoreAnnotations.*;

import com.opencsv.CSVReader;
import com.opencsv.CSVWriter;
import java.io.Reader;
import java.io.Writer;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class MyRun {

    public static StanfordCoreNLP pipeline;
    public static Properties props;
    public static Writer writer = null;
    public static CSVWriter csvWriter = null;

    public static String[] process(String id, String text) {

        CoreDocument document = new CoreDocument(text);

        // run all Annotators on this text
        pipeline.annotate(document);

        List<RelationTriple> relations = document.sentences().get(0).relations();
        //System.out.println("Example: relation");
        try {
            if(relations != null) {
                System.out.println("Relations:" + relations.get(0));
                System.out.println();
            }
        }
        catch(Exception e) {
            System.out.println("Relations error!!!");
        }

        String entsStr = "";
        String trueText = "";

        //System.out.println("Example: entity mentions");
        for(CoreSentence sent: document.sentences()) {
            List<CoreEntityMention> entityMentions = sent.entityMentions();
            for(CoreEntityMention entity: entityMentions) {
                String entText = entity.text();
                String entType = entity.entityType();
                String wikiTitle = "";
                if(entity.entity() != null) {
                    wikiTitle = entity.entity();
                }
                entsStr += entText + "#$#" + entType + "#$#" + wikiTitle + "$$$";
            }

            for (CoreLabel token: sent.tokens()) {
                String word = token.get(TextAnnotation.class);
                //String pos = token.get(PartOfSpeechAnnotation.class);
                //String ne = token.get(NamedEntityTagAnnotation.class);
                trueText += word + " ";
            }
        }

        /*
       // coreference between entity mentions
        CoreEntityMention originalEntityMention = document.sentences().get(0).entityMentions().get(1);
        System.out.println("Example: original entity mention");
        System.out.println(originalEntityMention);
        System.out.println("Example: canonical entity mention");
        System.out.println(originalEntityMention.canonicalEntityMention().get());
        System.out.println();
        */

        return new String[]{id, text, trueText, entsStr};
    }

    public static void main(String[] args) {

        String csvIFile = "../../processedText.csv";
        String csvOFile = "./TextWithEntities.csv";

        props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, truecase, pos, lemma, ner, entitylink");
        props.setProperty("truecase.overwriteText", "true");
        props.setProperty("ner.model", "../classifiers/english.all.3class.distsim.crf.ser.gz");
        props.setProperty("ner.applyNumericClassifiers", "false");
        props.setProperty("ner.combinationMode", "HIGH_RECALL");
        pipeline = new StanfordCoreNLP(props);

        try {
            writer = Files.newBufferedWriter(Paths.get(csvOFile));
            csvWriter = new CSVWriter(writer);
        }
        catch(Exception e) {
            System.out.println(e);
            return;
        }

        String[] headerRecord = {"Id", "Processed Text", "True Text", "Entities"};
        csvWriter.writeNext(headerRecord);

        try {
            Reader reader = Files.newBufferedReader(Paths.get(csvIFile));
            CSVReader csvReader = new CSVReader(reader);
            csvReader.readNext();

            String[] nextRecord;
            int count = 0;
            while ((nextRecord = csvReader.readNext()) != null) {
                if(count % 50000 == 0) {
                    System.out.println(count);
                }

                if(nextRecord.length != 3) {
                    System.out.println("Error");
                    break;
                }

                String[] res = process("0", "obama is visiting canada");
                csvWriter.writeNext(res);
                count += 1;
                break;
            }
        }
        catch(Exception e) {
            System.out.println(e);
        }

        try{
            csvWriter.close();
        }
        catch(Exception e) {
            System.out.println(e);
        }
        
    }
}